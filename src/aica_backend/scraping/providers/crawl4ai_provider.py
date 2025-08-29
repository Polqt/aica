import asyncio
import json
import logging
import time

from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.async_configs import LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

from .base import BaseProvider
from ...core.config import settings
from ...utils import scraping as scrape_utils

logger = logging.getLogger(__name__)

class Crawl4AIProvider(BaseProvider):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config.get('name', 'crawl4ai'), config)
        self.site_config = config
        self.browser_config = self._create_browser_config()
        self.rate_limit_delay = settings.SCRAPING_RATE_LIMIT_DELAY
        self.max_retries = settings.SCRAPING_MAX_RETRIES

    def _create_browser_config(self) -> BrowserConfig:
        return BrowserConfig(
            headless=self.site_config.get('browser_config', {}).get('headless', settings.CRAWL4AI_HEADLESS),
            browser_type=settings.CRAWL4AI_BROWSER_TYPE,
            user_agent=settings.CRAWL4AI_USER_AGENT
        )

    @staticmethod
    def _load_json_from_file(file_path: str) -> Dict[str, Any]:
        try:
            with open(Path(file_path), 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading JSON from {file_path}: {str(e)}")
            raise

    @staticmethod
    def _load_text_from_file(file_path: str) -> str:
        try:
            with open(Path(file_path), 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            logging.error(f"Error loading text from {file_path}: {str(e)}")
            raise

    def _create_extraction_strategy(self) -> LLMExtractionStrategy:
        llm_settings = self.site_config['llm_config']
        schema = self._load_json_from_file(llm_settings['schema_path'])
        instruction = self._load_text_from_file(llm_settings['prompt_path'])

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

    def scrape_job_listings(self) -> List[Dict[str, Any]]:
        return asyncio.run(self._scrape_site())

    async def _scrape_site(self) -> List[Dict[str, Any]]:
        all_jobs = []
        paginated_urls = self._get_paginated_urls(max_pages=2)

        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            # Process URLs one by one to avoid overwhelming the server
            for url in paginated_urls:
                jobs = await self._scrape_single_url(crawler, url)
                if jobs:
                    all_jobs.extend(jobs)
                # Add delay between requests
                await asyncio.sleep(self.rate_limit_delay)

        unique_jobs = self._remove_duplicates(all_jobs)
        return unique_jobs

    def _get_paginated_urls(self, max_pages: int = 5) -> List[str]:
        urls = []
        pagination_template = self.site_config.get('pagination_template', '')
        for base_url in self.site_config.get('base_urls', []):
            urls.append(base_url)
            if pagination_template:
                for page_num in range(2, max_pages + 1):
                    urls.append(base_url + pagination_template.format(page_num=page_num))

        return urls

    async def _scrape_single_url(self, crawler: AsyncWebCrawler, url: str) -> List[Dict[str, Any]]:
        """Scrape a single URL with simplified configuration."""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempting to scrape {url} (attempt {attempt + 1}/{self.max_retries})")
                
                # Simplified run config - start with basics
                run_config = CrawlerRunConfig(
                    extraction_strategy=self._create_extraction_strategy(),
                    wait_for=self.site_config.get('wait_for_selector', 'body'),
                    page_timeout=self.site_config.get('wait_for_timeout', 30000),
                    cache_mode=CacheMode.BYPASS
                )

                result = await crawler.arun(url=url, config=run_config)

                if result.success and result.extracted_content:
                    logger.info(f"Successfully scraped {url}")
                    return self._process_extracted_content(result.extracted_content, url)
                else:
                    logger.warning(f"Attempt {attempt + 1} failed for {url}: {result.error_message}")
                    
                    # If this is not the last attempt, wait before retrying
                    if attempt < self.max_retries - 1:
                        wait_time = (attempt + 1) * 2  # Exponential backoff
                        logger.info(f"Waiting {wait_time} seconds before retry...")
                        await asyncio.sleep(wait_time)
                        
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1} for {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All {self.max_retries} attempts failed for {url}")

        return []

    def _process_extracted_content(self, extracted_content: Any, source_url: str) -> List[Dict[str, Any]]:
        jobs = []

        try:
            data = json.loads(extracted_content) if isinstance(extracted_content, str) else extracted_content

            job_list = data.get('jobs', []) if isinstance(data, dict) else []

            for job_data in job_list:
                if isinstance(job_data, dict) and job_data.get('is_tech_job'):
                    cleaned_job = self._clean_job_data(job_data, source_url)
                    if cleaned_job:
                        jobs.append(cleaned_job)
                        
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            logger.error(f"Error processing extracted content from {source_url}: {str(e)}")
            logger.debug(f"Extracted content preview: {str(extracted_content)[:500]}...")

        logger.info(f"Processed {len(jobs)} tech jobs from {source_url}")
        return jobs

    def _clean_job_data(self, job_data: Dict[str, Any], source_url: str) -> Optional[Dict[str, Any]]:
        try:
            job_title = scrape_utils.clean_text(job_data.get('job_title', ''))
            company_name = scrape_utils.clean_text(job_data.get('company_name', ''))
            qualifications = job_data.get('qualifications', {})
            skills = qualifications.get('required_skills', [])

            if not job_title or not company_name:
                logger.debug(f"Skipping job due to missing title or company: {job_title} | {company_name}")
                return None

            raw_job_url = job_data.get('job_url')
            absolute_job_url = urljoin(source_url, raw_job_url) if raw_job_url else None

            return {
                'source_url': absolute_job_url,
                'source_site': self.name,
                'job_title': job_title,
                'company_name': company_name,
                'full_text': scrape_utils.clean_text(job_data.get('job_description', '')) +
                    "\n" + scrape_utils.clean_text(qualifications.get('full_text', '')),
                'location': scrape_utils.clean_text(job_data.get('location', '')),
                'employment_type': scrape_utils.normalize_employment_type(job_data.get('employment_type')),
                'experience_level': scrape_utils.normalize_experience_level(job_data.get('experience_level')),
                'all_skills': scrape_utils.clean_skills_array(skills),
                'tech_category': scrape_utils.categorize_tech_job(job_title, " ".join(skills)),
                'status': 'raw'
            }
        except Exception as e:
            logger.error(f"Error cleaning job data from {source_url}: {str(e)}")
            return None

    def _get_job_key(self, job: Dict[str, Any]) -> str:
        title = job.get('job_title', '').lower().strip()
        company = job.get('company_name', '').lower().strip()
        return f"{title}|{company}"

    def _remove_duplicates(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_keys = set()
        unique_jobs = []

        for job in jobs:
            job_key = self._get_job_key(job)
            if job_key not in seen_keys:
                seen_keys.add(job_key)
                unique_jobs.append(job)

        logger.info(f"Removed {len(jobs) - len(unique_jobs)} duplicate jobs")
        return unique_jobs