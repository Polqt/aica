import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from aica_backend.data.ingestion.base_scraper import ScrapingService

async def test_content_scraping():
    service = ScrapingService()
    
    print("📖 Testing content scraping with JSON storage...")
    print("⚠️ This will take longer as it extracts job content...")
    
    try:
        # Scrape only 5 jobs for testing
        json_file = await service.scrape_jobs_with_content("jobstreet", max_jobs=5)
        print(f"✅ Successfully scraped job content")
        print(f"📁 Saved to: {json_file}")
        
    except Exception as e:
        print(f"❌ Error during content scraping: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_content_scraping())