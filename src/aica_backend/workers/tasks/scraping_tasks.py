from ..celery_app import celery_app
from ...core.config import settings
from ...db.session import SessionLocal
from ...crud import crud_jobs
from crawl4ai import AsyncWebCrawler
import logging

JOB_SITES = {
    'JobStreet': '',
    'Indeed': '',
    'LinkedIn': '',
}

@celery_app.task(name='tasks.scrape_job_postings')
def scrape_job_postings():
    logging.info('Starting job scraping task...')
    crawler = AsyncWebCrawler(api_key=settings.CRAWL4AI_API_KEY)
    db = SessionLocal()

    for site_name, site_url in JOB_SITES.items():
        try:
            job_links = [site_url + "/sample-job-1" + "/sample-job-2"]

            for link in job_links:
                if crud_jobs.get_job_by_source_url(db, link):
                    logging.info(f"Skipping already existing job: {link}")
                    continue

                logging.info(f"Crawling new job: {link}")
                result = crawler.arun(site_url=link, target_format="markdown")

                if result and result.content:
                    job_data = {
                        "source_url": link,
                        "source_site": site_name,
                        "full_text": result.content,
                        "status_code": 200
                    }

                    crud_jobs.create_job_postings(db, job_data=job_data)
        except Exception as e:
            logging.error(f"Failed to scrape job: {e}")

    db.close()
    logging.info('Finished job scraping task.')
    return "Scraping job postings complete."