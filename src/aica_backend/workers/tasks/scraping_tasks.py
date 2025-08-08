import logging
import asyncio

from ..celery_app import celery_app
from ...core.config import settings
from ...db.session import SessionLocal
from ...crud import crud_jobs
from ...data.ingestion.base_scraper import ScrapingService
# from enrichment_tasks import enrich_job_with_llm

logging.basicConfig(level=logging.INFO)

@celery_app.task(bind=True, max_retries=3)
def scrape_site_jobs(self, site_name: str, pipeline_run_id: int = None):
    """
    Scrape job URLS from a specific job site
    1st step in the pipeline
    """
    try:
        logging.info(f"Starting scraping for site: {site_name}")
        
        scraping_service = ScrapingService()
        
        job_data = asyncio.run(scraping_service.scrape_site(site_name, extract_details=True))
        job_urls = [job['source_url'] for job in job_data if 'source_url' in job]
        
        if not job_urls:
            logging.warning(f"No job URLs found for {site_name}")
            return {"status": "completed", "jobs_found": 0}
        
        db = SessionLocal()
        try: 
            new_jobs_count = 0
            for url in job_urls:
                existing_job = crud_jobs.get_job_by_source_url(db, url=url)
                if not existing_job:
                    job = crud_jobs.create_job_posting(db, url=url, site=site_name)
                    new_jobs_count += 1
                    
                    extract_job_content.delay(job.id)
            
            logging.info(f"Created {new_jobs_count} new job records from {site_name}")
            return {
                "status": "completed",
                "jobs_found": len(job_urls),
                "new_jobs": new_jobs_count
            }    
        finally:
            db.close()    
                    
    except Exception as e:
        logging.error(f"Error scraping {site_name}: {str(e)}")
        raise self.retry(countdown=60 * (2 ** self.request.retries))

@celery_app.task(bind=True, max_retries=3)
def extract_job_content(self, job_id: int):
    """
    Extract full content from a job URL
    Updates job record with extracted content
    """
    db = SessionLocal()
    try:
        job = crud_jobs.get_job_by_id(db, job_id=job_id)
        if not job or job.status != 'raw':
            logging.warning(f"Job {job_id} not found or already processed")
            return
        
        logging.info(f"Extracting content for job {job_id}: {job.source_url}")
        
        scraping_service = ScrapingService()
        content = asyncio.run(scraping_service.extract_job_content(job.source_url))
        
        if content:
            job.full_text = content
            job.status = 'content_extracted'
            db.commit()
            
            logging.info(f"Successfully extracted content for job {job_id}")
            
            # enrich_job_with_llm.delay(job_id) Queue for LLM enrichment
        else:
            crud_jobs.update_job_status(db, job_id=job_id, status='extraction_failed')
            logging.error(f"Failed to extract content for job {job_id}")
    
    except Exception as e:
        logging.error(f"Error extracting content for {job_id}: {str(e)}")
        
        if self.request.retries >= self.max_retries:
            crud_jobs.update_job_status(db, job_id=job_id, status='extraction_failed')     
        else:
            raise self.retry(countdown=60 * (2 ** self.request.retries))
    finally:
        db.close()

@celery_app.task
def trigger_daily_scraping():
    """
    Trigger scraping for all ocnfigured job sites
    This task runs daily at 8:00 AM
    """
    job_sites = list(settings.JOB_SITES_CONFIG.keys())
    
    logging.info(f"Starting daily scraping for sites: {job_sites}")
    
    for site in job_sites:
        scrape_site_jobs.delay(site)
    
    return f"Triggered scraping for {len(job_sites)} sites"