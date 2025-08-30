import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

print("Starting test script...")

sys.path.insert(0, str(Path(__file__).parent / "src"))
print("Added src to path")

try:
    from aica_backend.core.config import settings
    print("Settings imported successfully")
except Exception as e:
    print(f"Failed to import settings: {e}")
    sys.exit(1)

try:
    from aica_backend.scraping.providers.crawl4ai_provider import Crawl4AIProvider
    from aica_backend.scraping.providers.factory import ScrapingProviderFactory
    print("Providers imported successfully")
except Exception as e:
    print(f"Failed to import providers: {e}")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jobstreet_scraping_test.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

import sys
import os
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

logger = logging.getLogger(__name__)

def _is_real_jobstreet_url(url: str) -> bool:
    """Check if URL is a real JobStreet job URL (not mock data)."""
    if not url or not isinstance(url, str):
        return False

    # Must contain jobstreet.com
    if "jobstreet.com" not in url.lower():
        return False

    if "/job/" not in url:
        return False

    if not url.startswith("https://"):
        return False

    if url.endswith(("/job/1", "/job/2", "/job/3", "/job/4", "/job/5")):
        return False

    url_parts = url.split("/job/")
    if len(url_parts) == 2:
        job_part = url_parts[1]
        if job_part.isdigit() or "-" in job_part or "_" in job_part:
            return True

    return False

def _validate_job_urls(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate that jobs have real, functional JobStreet URLs."""
    valid_jobs = []

    for job in jobs:
        job_url = job.get('job_url')
        if job_url and _is_real_jobstreet_url(job_url):
            valid_jobs.append(job)
        else:
            logger.warning(f"Invalid or mock URL for job: {job.get('job_title', 'Unknown')} - URL: {job_url}")

    return valid_jobs
print("Logging configured")

async def test_jobstreet_scraping():
    """Test scraping 300 jobs from JobStreet."""

    logger.info("Starting JobStreet scraping test...")

    job_sources_path = Path("src/aica_backend/job_sources.json")
    try:
        with open(job_sources_path, 'r') as f:
            job_sources_config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load job_sources.json: {e}")
        return

    # Get JobStreet configuration
    jobstreet_config = job_sources_config.get('sources', {}).get('jobstreet', {})
    if not jobstreet_config.get('active', False):
        logger.error("JobStreet source is not active in configuration")
        return

    logger.info("JobStreet configuration loaded successfully")

    provider_config = {
        'name': 'jobstreet',
        'active': True,
        'llm_config': jobstreet_config.get('llm_config', {}),
        'base_urls': jobstreet_config.get('base_urls', []),
        'pagination_template': jobstreet_config.get('pagination_template', ''),
        'browser_config': {
            'headless': True,
            'verbose': False,  # Disable verbose logging
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        },  # Simplified browser config
        'wait_for_selector': 'body',  # Use body selector instead of specific job card selector
        'wait_for_timeout': 30000,  # Reduced timeout for testing
        'rate_limit_delay': 3,  # Increased delay
        'max_retries': 2  # Reduced retries
    }

    logger.info(f"Provider config: {json.dumps(provider_config, indent=2)}")

    try:
        # Create the provider
        provider = ScrapingProviderFactory.create_provider('crawl4ai', provider_config)
        logger.info("Crawl4AI provider created successfully")

        # Test connection
        try:
            test_result = await provider.test_connection()
            logger.info(f"Connection test result: {test_result}")

            if not test_result.get('status') == 'success':
                logger.warning("Connection test failed, but continuing with scraping...")
        except Exception as e:
            logger.warning(f"Connection test error (continuing anyway): {e}")

        # Generate URLs to scrape (first few pages to test)
        base_url = "https://ph.jobstreet.com/jobs-in-information-communication-technology"
        urls = [base_url]

        # Add paginated URLs (start with fewer pages for testing)
        for page in range(2, 3):  # Just page 2 for initial test
            urls.append(f"{base_url}?page={page}")

        logger.info(f"Generated {len(urls)} URLs to scrape")

        # Start scraping
        start_time = datetime.now()
        logger.info(f"Starting scraping at {start_time}")

        try:
            jobs = await provider.scrape_jobs(urls)
            logger.info(f"Successfully scraped {len(jobs)} jobs")

            # Validate that we have real URLs, not mock data
            valid_jobs = []
            for job in jobs:
                job_url = job.get('job_url')
                if job_url and _is_real_jobstreet_url(job_url):
                    valid_jobs.append(job)
                else:
                    logger.warning(f"Skipping job with invalid/mock URL: {job.get('job_title', 'Unknown')} - URL: {job_url}")

            jobs = valid_jobs
            logger.info(f"Validated {len(jobs)} jobs with real JobStreet URLs")

            if len(jobs) < 300:
                logger.info(f"Only found {len(jobs)} jobs with real URLs, trying more pages...")
                additional_urls = []
                for page in range(3, 11):  
                    additional_urls.append(f"{base_url}?page={page}")

                if additional_urls:
                    logger.info(f"Trying {len(additional_urls)} additional pages...")
                    additional_jobs = await provider.scrape_jobs(additional_urls)

                    for job in additional_jobs:
                        job_url = job.get('job_url')
                        if job_url and _is_real_jobstreet_url(job_url) and job not in jobs:
                            jobs.append(job)

                    logger.info(f"Total jobs after additional pages: {len(jobs)}")

        except UnicodeEncodeError as e:
            logger.error(f"Unicode encoding error during scraping: {e}")
            logger.error("Cannot continue without proper encoding support")
            return []
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            logger.error("Scraping failed, cannot generate mock data as requested")
            return []

        end_time = datetime.now()
        duration = end_time - start_time

        logger.info(f"Scraping completed in {duration}")
        logger.info(f"Total jobs scraped: {len(jobs)}")

        # Filter for tech jobs only and validate URLs
        tech_jobs = [job for job in jobs if job.get('is_tech_job', True)]
        valid_tech_jobs = _validate_job_urls(tech_jobs)

        logger.info(f"Tech jobs found: {len(tech_jobs)}")
        logger.info(f"Tech jobs with valid URLs: {len(valid_tech_jobs)}")

        # Save results to JSON file
        output_file = "jobstreet_tech_jobs.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "scraped_at": end_time.isoformat(),
                    "duration_seconds": duration.total_seconds(),
                    "total_jobs_scraped": len(jobs),
                    "tech_jobs_found": len(tech_jobs),
                    "tech_jobs_with_valid_urls": len(valid_tech_jobs),
                    "urls_scraped": len(urls),
                    "target": 300
                },
                "jobs": valid_tech_jobs
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"Results saved to {output_file}")

        # Validate results
        if len(valid_tech_jobs) >= 300:
            logger.info("✅ SUCCESS: Scraped at least 300 tech jobs with real, functional URLs!")
        else:
            logger.warning(f"⚠️  WARNING: Only scraped {len(valid_tech_jobs)} tech jobs with valid URLs, target was 300")

        # Print sample jobs with URLs
        logger.info("Sample of scraped jobs with real URLs:")
        for i, job in enumerate(valid_tech_jobs[:5]):
            logger.info(f"Job {i+1}: {job.get('job_title')} at {job.get('company_name')}")
            logger.info(f"  URL: {job.get('job_url')}")

        return valid_tech_jobs

    except Exception as e:
        logger.error(f"Error during scraping test: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    # Check if Ollama is running
    try:
        import ollama
        ollama.list()
        logger.info("Ollama is running")
    except Exception as e:
        logger.error(f"Ollama not available: {e}")
        logger.error("Please start Ollama and ensure llama3 model is available")
        sys.exit(1)

    # Run the test
    result = asyncio.run(test_jobstreet_scraping())

    if result and len(result) >= 300:
        print("SUCCESS: Test PASSED - Successfully scraped 300+ tech jobs with real, functional URLs from JobStreet")
        sys.exit(0)
    else:
        print(f"FAILED: Test FAILED - Only scraped {len(result) if result else 0} tech jobs with valid URLs (target: 300)")
        sys.exit(1)