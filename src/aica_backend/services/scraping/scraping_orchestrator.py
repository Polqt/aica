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
                json_file = await self.scraper.scrape_jobs_with_content(site)
                results[site] = {"json_file": json_file, "status": "success"}
                logging.info(f"Completed scraping for {site}: {json_file}")
            except Exception as e:
                logging.error(f"Error scraping {site}: {e}")
                results[site] = {"error": str(e), "status": "failed"}
        return results
                       