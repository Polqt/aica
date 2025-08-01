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
                job_data = await self.scraper.scrape_site(site, extract_details=True, max_jobs=50)
                json_file = f"data/scraped_jobs/{site}_detailed_*.json"
                results[site] = {"json_file": json_file, "status": "success"}
                logging.info(f"Completed scraping for {site}: {json_file}")
            except Exception as e:
                logging.error(f"Error scraping {site}: {e}")
                results[site] = {"error": str(e), "status": "failed"}
        return results
                       