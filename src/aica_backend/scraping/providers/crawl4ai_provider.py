import asyncio
import logging

from datetime import datetime
from typing import List, Dict, Any, Optional
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from .base import BaseProvider

logger = logging.getLogger(__name__)

class Crawl4AIProvider(BaseProvider):
    def __init__(self, config: Dict[str, Any]):
        super().__init__('crawl4ai', config)
        
        self.browser_config = BrowserConfig(
            headless=config.get('headless', True),
            browser_type=config.get('browser_type', 'chromium'),
            viewport_width=config.get('viewport_width', 1920),
            viewport_height=config.get('viewport_height', 1080),
            user_agent=config.get('user_agent', 'AICA-JobBot/1.0 (Educational Research)')
        )
        self.rate_limit_delay  = config.get('rate_limit_delay', 2)
        self.max_retries = config.get('max_retries', 3)
        self.extraction_strategy = self._create_extraction_strategy()
        
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
            "required": ["job_title", "company_name", "job_description", "preferred_skills", "required_skills"]
        }
        
        instruction = """
            Extract job posting information from the provided content. Focus on:
            1. Job title and company name
            2. Location and employment type (full-time, part-time, contract, and etc.)
            3. Salary information if available
            4. Detailed job description
            5. Required and preferred skills (extract as separate arrays)
            6. Experience level and educational requirements
            7. Applicationd deadline and posting if available
        
            Be through and accurate. If information is not available, leave the field empty or null.
        """
        
        return LLMExtractionStrategy(
            provider="ollama",
            api_token=self.config_get("llm_api_token", ""),
            schema=schema,
            extraction_type="schema",
            instruction=instruction,
        )
        
    async def scrape_jobs(self, urls: List[str]) -> List[Dict[str, Any]]:
        jobs = []
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for url in urls:
                try:
                    logger.info(f"Scraping URL: {url}")
                    
                    await asyncio.sleep(self.rate_limit_delay)
                    
                    run_config = CrawlerRunConfig(
                        extraction_strategy=self.extraction_strategy,
                        js_code=[
                            "window.scrollTo(0, document.body.scrollHeight);",
                            "await new Promise(resolve => setTimeout(resolve, 2000));"
                        ],
                        wait_for="css:.job_listing, .job_card, [data-testid*='job']",
                        page_timeout=3000,
                        js_only=True,
                    )
                    
                    result = await crawler.arun(
                        url=url,
                        config=run_config,
                    )
                    
                    if result.sucess and result.extracted_content:
                        extracted_jobs = self._process_extracted_content(result.extracted_content, url)
                        jobs.extend(extracted_jobs)
                        logger.info(f"Successfully scraped {len(extracted_jobs)} jobs from {url}")
                    else:
                        logger.warning(f"Failed to scrape {url}: {result.errors}")
                        
                except Exception as e:
                    logger.error(f"Error scraping {url}: {str(e)}")
                    continue
        
        return jobs
    
    def _process_extracted_content(self, extracted_content: Any, source_url: str) -> List[Dict[str, Any]]:
        jobs = []
        
        try:
            if isinstance(extracted_content, list):
                job_data_list = extracted_content
            else:
                job_data_list = [extracted_content]
            
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
                'application_deadline': self._parse_date(job_data.get('application_deadline', '')),
                'posted_date': self._parse_date(job_data.get('posted_date', '')),
                'job_url': job_data.get('job_url', source_url),
                'source_url': source_url,
                'scraped_at': datetime.now().isoformat(),
                'provider': 'crawl4ai'
            }
            
            return cleaned_job
        
        except Exception as e:
            logger.error(f"Error cleaning job data from {source_url}: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return str(text) if text else ' '
        return text.strip().replace('\n', ' ').replace('\r', ' ')

    def _clean_skills_array(self, skills: List[str]) -> List[str]:
        if not isinstance(skills, list):
            return []
        return [self._clean_text(skill) for skill in skills if isinstance(skill, str) and self._clean_text(skill)]
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        if not date_str or not isinstance(date_str, str):
            return None
        
        try:
            return date_str.strip()
        except:
            return None
        
    async def get_supported_sites(self) -> List[str]:
        return [
            'indeed.com',
            'linkedin.com',
            'glassdoor.com',
            'monster.com',
            'careerbuilder.com',
        ]
    
    async def validate_site_access(self, url: str) -> bool:
        try:
            if not url.startswith('http://', 'https://'):
                return False
            
            supported_sites = await self.get_supported_sites()
            return any(site in url for site in supported_sites)
        except Exception as e:
            logger.error(f"Error validating site access for {url}: {str(e)}")
            return False
        
        
        