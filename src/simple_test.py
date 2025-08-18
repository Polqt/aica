import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.append(str(Path(__file__).parent))

try:
    from aica_backend.scraping.providers.crawl4ai_provider import Crawl4AIProvider
    REAL_SCRAPING = True
except ImportError:
    print("⚠️  Could not import Crawl4AIProvider. Using mock mode.")
    print("Make sure you're running from the src/ directory")
    REAL_SCRAPING = False

async def test_tech_job_scraping():
    """Test scraping technology jobs from Philippine job sites."""
    
    config = {
        'headless': True,
        'browser_type': 'chromium',
        'rate_limit_delay': 2,
        'max_retries': 3,
        'user_agent': 'AICA-JobBot/1.0 (Educational Research)',
        'llm_api_token': ''  # Add your Ollama token if needed
    }
    
    # Test URLs for Philippine tech jobs
    test_urls = [
        'https://www.jobstreet.com.ph/jobs/information-technology',
        'https://www.kalibrr.com/jobs?q=software+engineer&l=philippines',
        'https://www.linkedin.com/jobs/search/?keywords=developer%20philippines'
    ]
    
    print("🚀 Testing Technology Job Scraping")
    print("=" * 50)
    print(f"🌐 Testing {len(test_urls)} URLs")
    print(f"🔧 Real scraping: {'Yes' if REAL_SCRAPING else 'No (Mock mode)'}")
    print()
    
    if REAL_SCRAPING:
        provider = Crawl4AIProvider(config)
    else:
        # Mock provider for testing
        class MockProvider:
            async def scrape_jobs(self, urls):
                await asyncio.sleep(1)  # Simulate delay
                return [
                    {
                        'job_title': 'Software Engineer',
                        'company_name': 'Tech Corp',
                        'location': 'Cebu City',
                        'required_skills': ['Python', 'JavaScript'],
                        'provider': 'mock'
                    }
                ]
        provider = MockProvider()
    
    try:
        # Run the scraping
        jobs = await provider.scrape_jobs(test_urls)
        
        print(f"✅ Scraping completed!")
        print(f"📊 Total jobs found: {len(jobs)}")
        print()
        
        # Filter and display technology jobs
        tech_jobs = [job for job in jobs if is_tech_job(job)]
        
        print(f"🖥️  Technology jobs: {len(tech_jobs)}")
        print("-" * 30)
        
        for i, job in enumerate(tech_jobs[:5], 1):  # Show first 5
            print(f"{i}. {job.get('job_title', 'N/A')}")
            print(f"   🏢 Company: {job.get('company_name', 'N/A')}")
            print(f"   📍 Location: {job.get('location', 'N/A')}")
            skills = job.get('required_skills', [])
            print(f"   🔧 Skills: {', '.join(skills[:3]) if skills else 'N/A'}")
            print()
        
        # Save results
        if tech_jobs:
            output_file = 'tech_jobs_scraped.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tech_jobs, f, indent=2, ensure_ascii=False)
            print(f"💾 Results saved to: {output_file}")
        
        return tech_jobs
        
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        raise

def is_tech_job(job: Dict[str, Any]) -> bool:
    """Check if a job is technology-related."""
    tech_keywords = [
        'software', 'developer', 'engineer', 'programmer', 'analyst',
        'data', 'devops', 'cloud', 'cybersecurity', 'machine learning',
        'ai', 'database', 'system', 'network', 'it support',
        'information technology', 'computer science', 'full stack',
        'backend', 'frontend', 'mobile', 'web', 'architect'
    ]
    
    job_title = job.get('job_title', '').lower()
    job_desc = job.get('job_description', '').lower()
    
    return any(keyword in job_title or keyword in job_desc for keyword in tech_keywords)

if __name__ == "__main__":
    print("🤖 AICA Technology Job Scraper")
    print("Testing scraping for tech jobs in the Philippines\n")
    
    try:
        jobs = asyncio.run(test_tech_job_scraping())
        print(f"\n🎉 Test completed! Found {len(jobs)} technology jobs.")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed: {str(e)}")
        sys.exit(1)