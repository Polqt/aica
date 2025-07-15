import logging

from ..celery_app import celery_app
from ...core.config import settings
from ...db.session import SessionLocal
from ...crud import crud_jobs

from crawl4ai import AsyncWebCrawler
from langchain_core.pydantic_v1 import BaseModel, Field
from sentence_transformers import SentenceTransformer
from typing import List

# Models and Chains are initialized once per worker process
logging.basicConfig(level=logging.INFO)

class JobDetails(BaseModel):
    job_title: str = Field(description='The precise job title')
    company_name: str = Field(description='The name of the hiring company')
    extracted_skills: str = Field(description='A list of key skills that mentioned')



@celery_app.task(name="tasks.run_full_job_pipeline")
def run_full_job_pipeline():
    logging.info("Starting full job pipeline...")

    job_sites_to_scrape = ["JobStreet, Indeed, LinkedIn"]

    for site in job_sites_to_scrape:
        scrape_and_process_site.delay(site_name=site)
    return "Pipeline triggered for all sites"

@celery_app.task
def scrape_and_process_site(site_name: str):
    logging.info(f"Processing site: {site_name}")
    db = SessionLocal()

    new_job_urls = [""]

    for url in new_job_urls:
        if not crud_jobs.get_job_by_source_url(db, url=url):
            job = crud_jobs.create_job_posting(db, url=url, site=site_name)
            enrich_single_job.delay(job.id)
    db.close()

@celery_app.task(rate_limit="10/m")
def enrich_single_job(job_id: int):
    db = SessionLocal()
    job = crud_jobs.get_job_by_id(db, id=job_id)

    if not job or job.status != 'raw':
        db.close()
        return

    try:
        logging.info(f"Crawling job ID {job.id}: {job.source_url}")
    except Exception as e:
        logging.error(f"Failed to enrich job ID {job.id}, Error: {e}")
    finally:
        db.close()