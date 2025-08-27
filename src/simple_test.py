import asyncio
import json
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

sys.path.append(str(Path(__file__).resolve().parent.parent))

def check_imports():
    """Check if required modules can be imported"""
    try:
        from aica_backend.scraping.providers.crawl4ai_provider import Crawl4AIProvider
        from aica_backend.core.config import settings 
        print("âœ… Successfully imported required modules!")
        return True, Crawl4AIProvider, settings
    except ImportError as e:
        print(f"âŒ Import failed: {e}")
        print("ðŸ’¡ Run from project root and ensure crawl4ai is installed")
        return False, None, None

async def test_ollama_connection(settings):
    """Simple Ollama connection test"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model['name'] for model in data.get('models', [])]
                    print(f"ðŸ¦™ Ollama connected! Models: {models}")
                    
                    if settings.OLLAMA_MODEL_NAME in models:
                        print(f"âœ… Target model '{settings.OLLAMA_MODEL_NAME}' is available")
                        return True
                    else:
                        print(f"âŒ Model '{settings.OLLAMA_MODEL_NAME}' not found")
                        return False
                else:
                    print(f"âŒ Ollama returned status: {response.status}")
                    return False
    except Exception as e:
        print(f"âŒ Ollama connection failed: {e}")
        print(f"ðŸ’¡ Ensure Ollama is running at: {settings.OLLAMA_BASE_URL}")
        return False

async def test_job_scraping(provider, max_jobs: int = 10):
    """Test the improved scraping with validation"""
    print(f"\nðŸš€ Testing job scraping (max {max_jobs} jobs)")
    print("=" * 50)
    
    try:
        # Test URL generation
        search_urls = provider.get_tech_job_search_urls()
        print(f"ðŸ“‹ Testing with {len(search_urls)} search URLs:")
        for url in search_urls:
            print(f"   ðŸ“Œ {url}")
        
        # Run scraping
        jobs = await provider.scrape_all_jobs(max_jobs)
        
        if not jobs:
            print("âš ï¸  No jobs found - possible issues:")
            print("   â€¢ Network connectivity")
            print("   â€¢ Ollama not responding")
            print("   â€¢ JobStreet blocking requests")
            print("   â€¢ Website structure changed")
            return []
        
        # Analyze results
        print(f"\nðŸ“Š Results Summary:")
        print(f"   Total jobs found: {len(jobs)}")
        
        # Tech categories
        categories = {}
        for job in jobs:
            cat = job.get('tech_category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            print(f"   Tech categories:")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"     â€¢ {cat}: {count}")
        
        # Show sample jobs
        print(f"\nðŸ“ Sample Jobs (first {min(3, len(jobs))}):")
        print("-" * 50)
        
        for i, job in enumerate(jobs[:3], 1):
            print(f"{i}. {job.get('job_title', 'N/A')}")
            print(f"   ðŸ¢ {job.get('company_name', 'N/A')}")
            print(f"   ðŸ“ {job.get('location', 'N/A')}")
            print(f"   ðŸ’¼ {job.get('employment_type', 'N/A')}")
            
            skills = job.get('required_skills', [])
            if skills:
                skills_preview = ', '.join(skills[:3])
                if len(skills) > 3:
                    skills_preview += f" (+{len(skills)-3} more)"
                print(f"   ðŸ”§ Skills: {skills_preview}")
            
            print(f"   ðŸ”— URL: {job.get('job_url', 'N/A')}")
            print()
        
        # Data validation check
        valid_count = 0
        for job in jobs:
            if (job.get('job_title') and 
                job.get('company_name') and 
                job.get('job_url') and 
                job.get('is_tech_job')):
                valid_count += 1
        
        print(f"âœ… Data quality: {valid_count}/{len(jobs)} jobs have all required fields")
        
        # Save results
        output_file = 'improved_tech_jobs.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"ðŸ’¾ Results saved to: {output_file}")
        
        return jobs
        
    except Exception as e:
        print(f"âŒ Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    print("ðŸ¤– AICA Tech Job Scraper - Improved Version")
    print("=" * 50)
    
    # Check imports
    imports_ok, Crawl4AIProvider, settings = check_imports()
    if not imports_ok:
        sys.exit(1)
    
    # Test Ollama
    print("\nðŸ” Checking Ollama connection...")
    ollama_ok = asyncio.run(test_ollama_connection(settings))
    if not ollama_ok:
        print("\nâŒ Fix Ollama setup first:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Install model: ollama pull llama3:latest")
        sys.exit(1)
    
    # Create provider
    try:
        config = settings.model_dump()
        provider = Crawl4AIProvider(config)
        print("âœ… Provider initialized successfully")
    except Exception as e:
        print(f"âŒ Provider initialization failed: {e}")
        sys.exit(1)
    
    # Run scraping test
    TARGET_JOBS = 10  # Small number for testing
    jobs = asyncio.run(test_job_scraping(provider, TARGET_JOBS))
    
    # Final summary
    if jobs:
        print(f"\nðŸŽ‰ Test completed successfully!")
        print(f"ðŸ“ˆ Success rate: {len(jobs)}/{TARGET_JOBS} = {(len(jobs)/TARGET_JOBS)*100:.1f}%")
        
        # Quality metrics
        tech_jobs = sum(1 for job in jobs if job.get('is_tech_job'))
        complete_jobs = sum(1 for job in jobs if all([
            job.get('job_title'),
            job.get('company_name'),
            job.get('job_url'),
            job.get('location')
        ]))
        
        print(f"ðŸŽ¯ Tech jobs: {tech_jobs}/{len(jobs)} ({(tech_jobs/len(jobs))*100:.1f}%)")
        print(f"ðŸ“‹ Complete data: {complete_jobs}/{len(jobs)} ({(complete_jobs/len(jobs))*100:.1f}%)")
    else:
        print(f"\nâš ï¸  No jobs scraped - check the issues above")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nâ¹ï¸  Test interrupted by user")
    except Exception as e:
        print(f"\nðŸ’¥ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)