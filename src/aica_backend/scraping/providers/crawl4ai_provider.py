import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from urllib.parse import urljoin, urlparse

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.async_configs import LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

from .base import BaseProvider
from ...core.config import settings
from ...utils.robots_checker import SimpleRobotsChecker

logger = logging.getLogger(__name__)

class Crawl4AIProvider(BaseProvider):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config.get('name', 'crawl4ai'), config)
        self.site_config = config
        self.browser_config = self._create_browser_config()
        self.rate_limit_delay = settings.SCRAPING_RATE_LIMIT_DELAY
        self.max_retries = settings.SCRAPING_MAX_RETRIES
        self.robots_checker = SimpleRobotsChecker(user_agent=self.browser_config.user_agent)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def _create_browser_config(self) -> BrowserConfig:
        return BrowserConfig(
            headless=self.site_config.get('browser_config', {}).get('headless', settings.CRAWL4AI_HEADLESS),
            browser_type=settings.CRAWL4AI_BROWSER_TYPE,
            user_agent=self.site_config.get('browser_config', {}).get('user_agent', settings.CRAWL4AI_USER_AGENT),
            verbose=False  # Disable verbose logging to avoid encoding issues
        )

    @staticmethod
    def _load_json_from_file(file_path: str) -> Dict[str, Any]:
        try:
            base_path = Path(__file__).parent.parent.parent  
            full_path = base_path / file_path
            with open(full_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading JSON from {file_path}: {str(e)}")
            raise

    @staticmethod
    def _load_text_from_file(file_path: str) -> str:
        try:
            base_path = Path(__file__).parent.parent.parent  
            full_path = base_path / file_path
            with open(full_path, 'r') as f:
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

    async def _scrape_site(self) -> List[Dict[str, Any]]:
        all_jobs = []
        paginated_urls = self._get_paginated_urls(max_pages=2)

        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            for url in paginated_urls:
                jobs = await self._scrape_single_url(crawler, url)
                if jobs:
                    all_jobs.extend(jobs)
                await asyncio.sleep(self.rate_limit_delay)

        return self._remove_duplicates(all_jobs)

    async def scrape_jobs(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape job listings from given URLs."""
        logger.info(f"Crawl4AIProvider: Starting scrape_jobs with {len(urls)} URLs")
        return await self._scrape_site_from_urls(urls)

    async def get_supported_sites(self) -> List[str]:
        """Get list of supported site domains."""
        return ["jobstreet.com", "remoteok.com"]

    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to provider services."""
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                return {"status": "success", "message": "Connection successful"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _scrape_site_from_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape from provided URLs."""
        all_jobs = []

        for url in urls:
            if not await self.robots_checker.can_fetch(url):
                continue

            crawl_delay = await self.robots_checker.get_crawl_delay(url) or self.rate_limit_delay
            actual_delay = max(self.rate_limit_delay, crawl_delay)

            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                jobs = await self._scrape_single_url(crawler, url)
                if jobs:
                    all_jobs.extend(jobs)
                    if "jobstreet" in url.lower() and len(all_jobs) >= 300:
                        break

            await asyncio.sleep(actual_delay)

        return self._remove_duplicates(all_jobs)

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
                run_config = CrawlerRunConfig(
                    extraction_strategy=self._create_extraction_strategy(),
                    wait_for=self.site_config.get('wait_for_selector', 'body'),
                    page_timeout=self.site_config.get('wait_for_timeout', 30000),
                    cache_mode=CacheMode.BYPASS,
                    log_console=False,
                    screenshot=False
                )

                result = await crawler.arun(url=url, config=run_config)

                if result.success and result.extracted_content:
                    return self._process_extracted_content(result.extracted_content, url)

                if attempt < self.max_retries - 1:
                    await asyncio.sleep((attempt + 1) * 2)

            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep((attempt + 1) * 2)

        return []

    def _process_extracted_content(self, extracted_content: Any, source_url: str) -> List[Dict[str, Any]]:
        """Process extracted content and return list of jobs matching schema."""
        jobs = []

        try:
            if isinstance(extracted_content, str):
                data = json.loads(extracted_content)
            else:
                data = extracted_content

            job_list = data.get('jobs', []) if isinstance(data, dict) else data if isinstance(data, list) else []

            for job_data in job_list:
                if isinstance(job_data, dict) and job_data.get('is_tech_job', False):
                    if job_data.get('job_title') and job_data.get('company_name'):
                        job_url = job_data.get('job_url')
                        if job_url:
                            job_url = self._validate_and_clean_url(job_url, source_url)
                            job_data['job_url'] = job_url

                        if "jobstreet" in source_url.lower():
                            if job_url and self._is_valid_jobstreet_url(job_url):
                                jobs.append(job_data)
                        else:
                            jobs.append(job_data)

        except (json.JSONDecodeError, TypeError, KeyError):
            return []

        return jobs

    def _validate_and_clean_url(self, url: str, source_url: str) -> Optional[str]:
        """Validate and clean extracted URLs."""
        if not url:
            return None

        url = url.strip()

        if url.startswith('/'):
            url = urljoin(source_url, url)
        elif not url.startswith('http'):
            url = urljoin(source_url, url)

        try:
            parsed = urlparse(url)
            return url if parsed.scheme and parsed.netloc else None
        except Exception:
            return None

    def _is_valid_jobstreet_url(self, url: str) -> bool:
        """Check if URL is a valid JobStreet job URL."""
        return bool(url and "jobstreet.com" in url.lower() and "/job/" in url)

    def _remove_duplicates(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate jobs based on title and company."""
        seen_keys = set()
        unique_jobs = []

        for job in jobs:
            job_key = f"{job.get('job_title', '').lower()}|{job.get('company_name', '').lower()}"
            if job_key not in seen_keys:
                seen_keys.add(job_key)
                unique_jobs.append(job)

        return unique_jobs