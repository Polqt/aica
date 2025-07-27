import logging
import asyncio

from ...data.ingestion.base_scraper import ScrapingService

class ScrapingOrchestrator:
    def __init__(self):
        self.scraper = ScrapingService()
        
    async def run_daily_scraping(self):
        sites = ['jobstreet']
        results = {}
        
        for site in sites:
            try:
                urls = asyncio.run(self.scraper.get_search_urls(site))
                results[site] = len(urls)
                logging.info(f"Scraped {len(urls)} job from {site}")
            except Exception as e:
                logging.error(f"Error scraping {site}: {e}")
                results[site] = 0
        return results
                       