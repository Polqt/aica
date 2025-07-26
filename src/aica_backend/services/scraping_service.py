# Purpose: Abstract scraping logic with different strategies for each job site
# Components:
# - BaseScraper (abstract class)
# - JobStreetScraper, IndeedScraper, LinkedInScraper
# - ScrapeStrategy enum
# - Rate limiting and retry logic

import asyncio
import aiohttp
import logging
import re
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ..core.config import settings
from typing import List, Dict, Optional

class ScrapingService:
    def __init__(self):
        self.sites_config = settings.JOB_SITES_CONFIG
    
    async def scrape_site(self, site_name: str) -> List[str]:
        # Site-specific scraping logic
        # Rate limiting per site
        # URL extraction and filtering
        if site_name not in self.sites_config:
            logging.error(f"Site {site_name} not configured")
            return []

        site_config = self.sites_config[site_name]
        base_url = site_config["base_url"]
        search_urls = site_config[search_urls]
        
        all_job_urls = []
        
        async with AsyncWebCrawler() as crawler:
            for search_path in search_urls:
                try:
                    search_url =  urljoin[base_url, search_path]
                    logging.info(f"Scraping search page: {search_url}")
                    
                    result = await crawler.arun(
                        url=search_url,
                        headers=site_config.get("headers", {}),
                        wait_for_selector=site_config["selectors"["job_links"]],
                        timeout=30000
                    )
                
                    if result.success:
                        job_urls = self._extract_job_urls(result.html, site_config, base_url)
                        all_job_urls.extend(job_urls)
                        logging.info(f"Found {len(job_urls)} jobs on {search_url}")
                        
                        await asyncio.sleep(60 / site_config["rate_limit"])
                    else:
                        logging.error(f"Failed to scrape {search_url}: {result.error_message}")
                except Exception as e:
                    logging.error(f"Error scraping {search_url}: {str(e)}")
                    continue
                
        unique_urls = list(set(all_job_urls))
        tech_urls = self._filter_tech_jobs(unique_urls)
        
        logging.info(f"Scraped {len*tech_urls} tech job URLs from {site_name}")
        return tech_urls
    
    async def extract_job_content(self, url: str) -> str:
        # crawl4ai integration
        # Content cleaning and extraction
        # Error handling for failed scrapes
        try:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(
                    url=url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                    timeout=30000,
                    wait_for_selector="body"
                )
                
                if result.success:
                    # Extract the content
                    soup = BeautifulSoup(result.html, 'html.parser')
                    
                    for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
                        element.decompose()
                    
                    # Get main content
                    text = soup.get_text()
                    
                    # Clean whitespace and normalize
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    return text[:10000] # Limit to 10k characters
                else:
                    logging.error(f"Failed to extract content from {url}: {result.error_message}")
                    return ""
        except Exception as e:
            logging.error(f"Error extracting content from {url}: {str(e)}")
            return ""
            
    async def get_search_urls(self, site_name: str) -> List[str]:
        # Generate search URLs based on configuration
        pass