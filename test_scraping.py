import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from aica_backend.data.ingestion.base_scraper import ScrapingService

async def test_scraping():
    service = ScrapingService()
    
    # Test JobstreetPH scraping
    print("Testing JobstreetPH scraping...")
    try:
        urls = await service.scrape_site("jobstreet")
        if urls:
            print("Testing content extraction...")
            content = await service.extract_job_content(urls[0])
            print(f"Extracted content length: {len(content)} characters")
            print(f"First 200 characters: {content[:200]}...")
        else:
            print("No job URLs found to text content extraction.")
    except Exception as e:
        print(f"Error during scraping: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_scraping())
                