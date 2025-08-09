import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from aica_backend.services import ScrapingService

async def test_scraping():
    service = ScrapingService()
    
    # Test JobstreetPH scraping
    print("Testing JobstreetPH scraping...")
    try:
        print("\n📋 Test 1: Search URL Generation")
        search_urls = await service.get_search_urls("jobstreet")
        print(f"✅ Generated {len(search_urls)} search URLs")
        for i, url in enumerate(search_urls[:3]):
            print(f"   {i+1}. {url}")
        
        # Test 2: URL-only scraping (fast test)
        print("\n📊 Test 2: URL-only scraping")
        urls_only = await service.scrape_site("jobstreet", extract_details=False, max_jobs=5)
        print(f"✅ Found {len(urls_only)} job URLs")
        
        # Test 3: Structured data extraction (limited)
        print("\n🎯 Test 3: Structured data extraction (2 jobs)")
        structured_jobs = await service.scrape_site("jobstreet", extract_details=True, max_jobs=2)
        
        print(f"✅ Extracted {len(structured_jobs)} structured job records")
        
        # Analyze extraction results
        if structured_jobs:
            print("\n📊 Extraction Analysis:")
            
            # Count successful extractions
            successful = [job for job in structured_jobs if job.get('extraction_quality_score', 0) > 0.5]
            print(f"   High-quality extractions: {len(successful)}/{len(structured_jobs)}")
            
            # Show sample extracted data
            print("\n📋 Sample Job Data:")
            for i, job in enumerate(structured_jobs[:2]):
                print(f"\n   Job {i+1}:")
                print(f"   Title: {job.get('job_title', 'N/A')}")
                print(f"   Company: {job.get('company_name', 'N/A')}")
                print(f"   Location: {job.get('location', 'N/A')}")
                print(f"   Work Type: {job.get('work_type', 'N/A')}")
                print(f"   Salary: {job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')} {job.get('salary_currency', '')}")
                print(f"   Skills: {job.get('technical_skills', [])[:5]}...")
                print(f"   Quality Score: {job.get('extraction_quality_score', 0)}")
        
    except Exception as e:
        print(f"❌ Error during structured scraping: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_scraping())
                