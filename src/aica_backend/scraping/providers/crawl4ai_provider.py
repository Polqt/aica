import asyncio
import logging

from datetime import datetime
from typing import List, Dict, Any, Optional
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

from .base import BaseProvider

logger = logging.getLogger(__name__)

class Crawl4AIProvider(BaseProvider):
    def __init__(self, config: Dict[str, Any]):
        super().__init__('crawl4ai', config)
        self.browser_config = self._create_browser_config(config)
        self.rate_limit_delay  = config.get('rate_limit_delay', 2)
        self.max_retries = config.get('max_retries', 3)
        
    def _create_browser_config(self, config: Dict[str, Any]) -> BrowserConfig:
        return BrowserConfig(
            headless=config.get('headless', True),
            browser_type=config.get('browser_type', 'chromium'),
            viewport_width=config.get('viewport_width', 1920),
            viewport_height=config.get('viewport_height', 1080),
            user_agent=config.get('user_agent', 'AICA-JobBot/1.0 (Educational Research)')
        )
        
    def _create_extraction_strategy(self) -> LLMExtractionStrategy:
        schema = {
            "type": "object",
            "properties": {
                "job_title": {"type": "string"},
                "company_name": {"type": "string"},
                "location": {"type": "string"},
                "employment_type": {"type": "string"},
                "salary_range": {"type": "string"},
                "job_description": {"type": "string"},
                "required_skills": {"type": "array", "items": {"type": "string"}},
                "preferred_skills": {"type": "array", "items": {"type": "string"}},
                "experience_level": {"type": "string"},
                "education_requirements": {"type": "string"},
                "application_deadline": {"type": "string"},
                "job_url": {"type": "string"},
                "posted_date": {"type": "string"}
            },
            "required": ["job_title", "company_name", "job_description"]
        }
        
        instruction = """
            Extract job posting information focusing on technology roles in:
            - Computer Science, Computer Engineering
            - Information Technology, Information Systems
            - Software Development, Data Science, Cybersecurity
            - Cloud Engineering, DevOps, AI/ML Engineering
            - Data Engineering, Data Analyst, Machine Learning Engineer
            - IT Support, Business System Analyst, Technical Writer
            - System Architecture, Network Engineer, Database Administrator
            - Mobile App Developer, Software Architect, Full Stack Developer
            - Backend Developer, Frontend Developer
            - Network Administrator, System Administrator, Cloud Architect,
            - UI/UX Designer, Technical Support Specialist, Project Manager

            Extract this important information below: 
            1. Job title and company name
            2. Location and employment type (full-time, part-time, contract, and etc.)
            3. Salary information if available
            4. Detailed job description
            5. Required and preferred skills (must have technical skills or soft skills)
            6. Experience level and educational requirements
            7. Application deadline and posting if available
        
            Be through and accurate. If information is not available, leave the field empty or null.
        """
        
        llm_config = LLMConfig(
            provider="ollama",
            api_token=self.config.get("llm_api_token", ""),
            model="llama3:latest"   
        )
        
        return LLMExtractionStrategy(
            llm_config=llm_config,
            schema=schema,
            extraction_type="schema",
            instruction=instruction,
        )
        
    def scrape_job_listings(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        urls = search_params.get('urls', [])
        return asyncio.run(self.scrape_jobs(urls))
    
    def scrape_job_details(self, job_url: str) -> Optional[Dict[str, Any]]:
        jobs = asyncio.run(self.scrape_jobs([job_url]))
        return jobs[0] if jobs else None
    
        
    async def scrape_jobs(self, urls: List[str]) -> List[Dict[str, Any]]:
        if not urls:
            return []
        
        jobs = []
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for url in urls:
                if not await self._validate_url(url):
                    logger.warning(f"Skipping invalid URL: {url}")
                    continue
                
                try:
                    logger.info(f"Scraping URL: {url}")
                    await asyncio.sleep(self.rate_limit_delay)
                    
                    job_data = await self._scrape_single_url(crawler, url)
                    
                    if job_data:
                        jobs.extend(job_data)
                        logger.info(f"Successfully scraped {len(job_data)} jobs from {url}")
                    
                        
                except Exception as e:
                    logger.error(f"Error scraping {url}: {str(e)}")
                    continue
        
        return jobs
    
    async def _scrape_single_url(self, crawler: AsyncWebCrawler, url: str) -> List[Dict[str, Any]]:
        run_config = CrawlerRunConfig(
            extraction_strategy=self._create_extraction_strategy(),
            js_code=[
                "window.scrollTo(0, document.body.scrollHeight);",
                "await new Promise(resolve => setTimeout(resolve, 2000));"
            ],
            wait_for="css:.job_listing, .job_card, [data-testid*='job']",
            page_timeout=30000,
            js_only=True,
        )
                    
        result = await crawler.arun(
            url=url,
            config=run_config,
        )
        
        if result.success and result.extracted_content:
            return self._process_extracted_content(result.extracted_content, url)
        else: 
            logger.warning(f"Failed to scrape {url}: {getattr(result, 'error_message', 'Unknown error')}")
            return []
                
    def _process_extracted_content(self, extracted_content: Any, source_url: str) -> List[Dict[str, Any]]:
        jobs = []
        
        try:
            job_data_list = extracted_content if isinstance(extracted_content, list) else [extracted_content]
            
            for job_data in job_data_list:
                if not isinstance(job_data, dict):
                    continue
                
                cleaned_job = self._clean_job_data(job_data, source_url)
                if cleaned_job:
                    jobs.append(cleaned_job)
                    
        except Exception as e:
            logger.error(f"Error processing extracted content from {source_url}: {str(e)}")
        
        return jobs

    def _clean_job_data(self, job_data: Dict[str, Any], source_url: str) -> Optional[Dict[str, Any]]:
        try:
            if not job_data.get("job_title") or not job_data.get("company_name"):
                return None
            
            cleaned_job = {
                'job_title': self._clean_text(job_data.get('job_title', '')),
                'company_name': self._clean_text(job_data.get('company_name', '')),
                'location': self._clean_text(job_data.get('location', '')),
                'employment_type': self._clean_text(job_data.get('employment_type', '')),
                'salary_range': self._clean_text(job_data.get('salary_range', '')),
                'job_description': self._clean_text(job_data.get('job_description', '')),
                'required_skills': self._clean_skills_array(job_data.get('required_skills', [])),
                'preferred_skills': self._clean_skills_array(job_data.get('preferred_skills', [])),
                'experience_level': self._clean_text(job_data.get('experience_level', '')),
                'education_requirements': self._clean_text(job_data.get('education_requirements', '')),
                'application_deadline': self._clean_text(job_data.get('application_deadline', '')),
                'posted_date': self._clean_text(job_data.get('posted_date', '')),
                'job_url': job_data.get('job_url', source_url),
                'source_url': source_url,
                'scraped_at': datetime.now().isoformat(),
                'provider': self.name
            }
            
            return cleaned_job
        
        except Exception as e:
            logger.error(f"Error cleaning job data from {source_url}: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ''
        return text.strip().replace('\n', ' ').replace('\r', ' ')

    def _clean_skills_array(self, skills: List[str]) -> List[str]:
        if not isinstance(skills, list):
            return []
        return [self._clean_text(skill) for skill in skills if isinstance(skill, str) and self._clean_text(skill)]
    
    async def _validate_url(self, url: str) -> bool:
        if not url or not (url.startswith('http://') or url.startswith('https://')):
            return False
        
        supported_sites = await self.get_supported_sites()
        return any(site in url.lower() for site in supported_sites)

        
    async def get_supported_sites(self) -> List[str]:
        return [
            'indeed.com',
            'linkedin.com',
            'glassdoor.com',
            'monster.com',
            'careerbuilder.com',
            'jobstreet.com.ph',
            'kalibrr.com'
        ]
        
    def get_test_url(self) -> str:
        return "https://www.jobstreet.com.ph/jobs/information-technology"