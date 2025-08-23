import asyncio
import json
import logging

from datetime import datetime
from typing import List, Dict, Any, Optional
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.async_configs import LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from urllib.parse import urljoin

from .base import BaseProvider
from ...core.config import settings
from ...utils import scraping as scrape_utils

logger = logging.getLogger(__name__)

class Crawl4AIProvider(BaseProvider):
    def __init__(self, config: Dict[str, Any]): 
        super().__init__('crawl4ai', config)
        self.browser_config = self._create_browser_config(config)
        self.rate_limit_delay  = settings.SCRAPING_RATE_LIMIT_DELAY
        self.max_retries = settings.SCRAPING_MAX_RETRIES
        
    def _create_browser_config(self, config: Dict[str, Any]) -> BrowserConfig:
        return BrowserConfig(
            headless=settings.CRAWL4AI_HEADLESS,
            browser_type=settings.CRAWL4AI_BROWSER_TYPE,
            user_agent=settings.CRAWL4AI_USER_AGENT
        )
        
    def _create_extraction_strategy(self) -> LLMExtractionStrategy:
        schema = {
            "type": "object", "properties": {"jobs": {"type": "array", "items": {
                "type": "object", "properties": {
                    "job_title": {"type": "string"},
                    "company_name": {"type": "string"},
                    "location": {"type": "string"},
                    "employment_type": {"type": "string"},
                    "job_description": {"type": "string"},
                    "required_skills": {"type": "array", "items": {"type": "string"}},
                    "experience_level": {"type": "string"},
                    "job_url": {"type": "string", "description": "The direct URL to the detailed job posting page"},
                    "is_tech_job": {"type": "boolean"}
                },
                "required": ["job_title", "company_name", "job_url", "is_tech_job"]
            }}},
            "required": ["jobs"]
        }
        
        instruction = """
            Extract job posting information focusing on the technology roles listed below.
            For each job posting you find on the page, extract the following details accurately.
            
            TARGET ROLES:
            - Software Development (Frontend, Backend, Full Stack, Mobile, Web)
            - Data & AI (Data Scientist, Data Engineer, ML Engineer)
            - Infrastructure & DevOps (DevOps Engineer, Cloud Engineer, SRE)
            - Cybersecurity (Security Analyst, Security Engineer)
            - IT Support & Management (IT Support, Systems Analyst)
            - Specialized Tech (QA Engineer, UI/UX Designer, Tech Product Manager)

            EXTRACTION RULES:
            1.  **is_tech_job**: Set to `true` ONLY if the role is clearly a technology job. Exclude general sales, marketing, and HR roles.
            2.  **job_url**: This is critical. You MUST extract the specific and unique URL that leads to the detailed page for EACH job. Do not reuse URLs between different job postings.
            3.  **Skills**: Extract a detailed list of technical skills like programming languages, frameworks, and tools.
            4.  **Accuracy**: Ensure the company name, location, and description match the correct job title.

            Return all technology-related jobs you find in the "jobs" array. Be thorough and precise.
        """
        
        llm_config = LLMConfig(
            provider=f"ollama/{settings.OLLAMA_MODEL_NAME}",
            base_url=settings.OLLAMA_BASE_URL, 
            temperature=0
        )
        
        return LLMExtractionStrategy(
            llm_config=llm_config,
            schema=schema,
            extraction_type="schema",
            instruction=instruction,
        )
        
    def get_tech_job_search_urls(self) -> Dict[str, List[str]]:
        return {
            'job_street': [
                'https://www.jobstreet.com.ph/jobs/software-developer',
                'https://www.jobstreet.com.ph/jobs/data-scientist',
                'https://www.jobstreet.com.ph/jobs/web-developer',
                'https://www.jobstreet.com.ph/jobs/mobile-developer',
            ],
            # 'kalibrr': [
            #     'https://www.kalibrr.com/jobs?q=software+engineer',
            #     'https://www.kalibrr.com/jobs?q=data+scientist',
            #     'https://www.kalibrr.com/jobs?q=web+developer',
            #     'https://www.kalibrr.com/jobs?q=mobile+developer',
            #     'https://www.kalibrr.com/jobs?q=devops',
            #     # 'https://www.kalibrr.com/jobs?q=cybersecurity',
            #     # 'https://www.kalibrr.com/jobs?q=full+stack',
            #     # 'https://www.kalibrr.com/jobs?q=backend+developer',
            #     # 'https://www.kalibrr.com/jobs?q=frontend+developer',
            #     # 'https://www.kalibrr.com/jobs?q=database',
            # ],
            # 'indeed': [
            #     # 'https://ph.indeed.com/jobs?q=software+engineer',
            #     # 'https://ph.indeed.com/jobs?q=data+analyst',
            #     # 'https://ph.indeed.com/jobs?q=web+developer',
            #     # 'https://ph.indeed.com/jobs?q=IT+support',
            #     # 'https://ph.indeed.com/jobs?q=system+administrator',
            #     'https://ph.indeed.com/jobs?q=cybersecurity',
            #     'https://ph.indeed.com/jobs?q=devops',
            #     'https://ph.indeed.com/jobs?q=database+administrator',
            #     'https://ph.indeed.com/jobs?q=mobile+developer',
            #     'https://ph.indeed.com/jobs?q=cloud+engineer',
            # ]
        }

    def scrape_job_listings(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        max_total_jobs = search_params.get('max_total_jobs', 300)
        return asyncio.run(self.scrape_all_jobs(max_total_jobs))
    
    async def scrape_all_jobs(self, max_total_jobs: int = 300) -> List[Dict[str, Any]]:
        all_jobs = []
        search_urls = self.get_tech_job_search_urls()
        
        logger.info(f"Starting scraping for tech jobs from {len(search_urls)} sites...")
        
        urls_to_scrape = []
        for site_name, base_urls in search_urls.items():
            for base_url in base_urls:
                paginated_urls = self._get_paginated_urls(base_url, site_name, max_pages=3)
                for url in paginated_urls:
                    urls_to_scrape.append({'url': url, 'site_name': site_name})
        
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            tasks = [
                self._scrape_single_url(crawler, item['url'], item['site_name'])
                for item in urls_to_scrape
            ]
            
            results = await asyncio.gather(*tasks)
        
        for job_list in results:
            if job_list:
                all_jobs.extend(job_list)

        unique_jobs = self._remove_duplicates(all_jobs)
        logger.info(f"Scraping completed! Total unique tech jobs: {len(unique_jobs)}")
        return unique_jobs[:max_total_jobs]
    
    async def _scrape_site(self,
                           crawler: AsyncWebCrawler,
                           base_url: str,
                           site_name: str) -> List[Dict[str, Any]]:
        
        site_jobs = []
        paginated_url = self._get_paginated_urls(base_url, site_name)
        
        for page_url in paginated_url[:3]:
            try:
                jobs_from_page = await self._scrape_single_url(crawler, page_url, site_name)
                if jobs_from_page:
                    site_jobs.extend(jobs_from_page)
                
                await asyncio.sleep(self.rate_limit_delay)
            except Exception as e:
                logger.error(f"Error scraping {page_url}: {str(e)}")
        
        return site_jobs
            
    def _get_job_key(self, job: Dict[str, Any]) -> str:
        title = job.get('job_title', '').lower().strip()
        company = job.get('company_name', '').lower().strip()
        location = job.get('location', '').lower().strip()
        return f"{title}|{company}|{location}"
    
    def _get_paginated_urls(self, base_url: str, site_name: str, max_pages: int = 5) -> List[str]:
        
        urls = [base_url]
        
        try:
            for page in range(2, max_pages + 1):
                if 'jobstreet' in site_name:
                    urls.append(f"{base_url}?page={page}") 
                elif 'kalibrr' in site_name:
                    separator = '&' if '?' in base_url else '?'
                    urls.append(f"{base_url}{separator}page={page}")
                elif 'indeed' in site_name:
                    start_index = (page - 1) * 10
                    separator = '&' if '?' in base_url else '?'
                    urls.append(f"{base_url}{separator}start={start_index}")  
        except Exception as e:
            logger.warning(f"Could not generate pagination for {base_url}: {e}")
            
        return urls
    
    async def _scrape_single_url(self, crawler: AsyncWebCrawler, url: str, site_name: str) -> List[Dict[str, Any]]:
        wait_for_selector = 'css:[data-automation="jobListing"]' if site_name == 'jobstreet' else 'body'
        
        run_config = CrawlerRunConfig(
            extraction_strategy=self._create_extraction_strategy(),
            wait_for=wait_for_selector,
            page_timeout=60000,
            delay_before_return_html=5
        )
        
        try:
            logger.info(f"Scraping {url} for {site_name}...")
            result = await crawler.arun(
                url=url,
                config=run_config
            )
            
            if result.success and result.extracted_content:
                jobs = self._process_extracted_content(result.extracted_content, url, site_name)
                return jobs
            else:
                logger.warning(f"Failed to scrape {url} for {site_name}: {result.error_message}")
                return []
        except Exception as e:
            logger.error(f"Error scraping {url} for {site_name}: {str(e)}")
            return []
                
    def _process_extracted_content(self, extracted_content: Any, source_url: str, site_name: str) -> List[Dict[str, Any]]:
        jobs = []
        
        try:
            data = json.loads(extracted_content) if isinstance(extracted_content, str) else extracted_content
            
            job_list = []
            
            if isinstance(data, dict):
                job_list = data.get('jobs', [])
            elif isinstance(data, list):
                job_list = data
               
            for job_data in job_list:
                if isinstance(job_data, dict) and job_data.get('is_tech_job'):
                    cleaned_job = self._clean_job_data(job_data, source_url, site_name)
                    if cleaned_job:
                        jobs.append(cleaned_job)
        except (json.JSONDecodeError, TypeError) as e:
            logger.error(f"Error processing extracted content from {source_url}: {str(e)}")
        
        return jobs

    def _clean_job_data(self, job_data: Dict[str, Any], source_url: str, site_name: str) -> Optional[Dict[str, Any]]:
        try:
            job_title = scrape_utils.clean_text(job_data.get('job_title', ''))
            company_name = scrape_utils.clean_text(job_data.get('company_name', ''))
            description = scrape_utils.clean_text(job_data.get('job_description', ''))
            
            raw_job_url = job_data.get('job_url')
            absolute_job_url = urljoin(source_url, raw_job_url) if raw_job_url else None
            
            if not job_title or not company_name:
                return None
            
            cleaned_job = {
                'job_title': job_title,
                'company_name': company_name,
                'location': scrape_utils.clean_text(job_data.get('location')),
                'employment_type': scrape_utils.normalize_employment_type(job_data.get('employment_type')),
                'experience_level': scrape_utils.normalize_experience_level(job_data.get('experience_level')),
                'job_description': description,
                'required_skills': scrape_utils.clean_skills_array(job_data.get('required_skills')),
                'job_url': absolute_job_url,
                'source_url': source_url,
                'source_site': site_name,
                'scraped_at': datetime.now().isoformat(),
                'provider': self.name,
                'tech_category': scrape_utils.categorize_tech_job(job_title, description)
            }
            
            return cleaned_job
        
        except Exception as e:
            logger.error(f"Error cleaning job data from {source_url}: {str(e)}")
            return None
    
    def _remove_duplicates(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_keys = set()
        unique_jobs = []
        
        for job in jobs:
            job_key = self._get_job_key(job)
            if job_key not in seen_keys:
                seen_keys.add(job_key)
                unique_jobs.append(job)
                
        return unique_jobs
             