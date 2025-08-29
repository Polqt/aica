import logging

from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session

from database.models import JobPosting, PipelineRun, ScrapingSession
from scraping.providers.factory import ScrapingProviderFactory
from utils.common import handle_service_error, create_success_response, AppError

logger = logging.getLogger(__name__)

class ScrapingService:
    def __init__(self, db: Session):
        self.db = db
        self.providers = {}
        self._initialize_providers()
        
    def _initialize_providers(self):
        provider_configs = {
            'crawl4ai': {
                'active': True,
                'headless': True,
                'rate_limit_delay': 2,
                'max_retries': 5
            },
            'beautifulsoup': {
                'active': True,
                'rate_limit_delay': 1,
                'max_retries': 3,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        for name, config in provider_configs.items():
            if config.get('active', False):
                try:
                    provider = ScrapingProviderFactory.create_provider(name, config)
                    self.providers[name] = provider
                    logger.info(f"Initialized provider: {name}")
                except Exception as e:
                    logger.error(f"Failed to initialize provider {name}: {e}")
                    
    async def start_scraping_pipeline(self, urls: List[str]) -> Dict[str, Any]:
        pipeline_run = PipelineRun(
            status="running",
            started_at=datetime.now()
        )
        
        self.db.add(pipeline_run)
        self.db.commit()
        
        try:
            results = await self._execute_scraping(pipeline_run.id, urls)
            
            pipeline_run.status = "completed"
            pipeline_run.completed_at = datetime.now()
            pipeline_run.total_jobs_scraped = results["total_scraped"]
            pipeline_run.total_jobs_processed = results["total_processed"]
            self.db.commit()
            
            return create_success_response({
                "pipeline_run_id": pipeline_run.id,
                "results": results
            })
        except Exception as e:
            logger.error(f"Error during scraping pipeline: {e}")
            pipeline_run.completed_at = datetime.now()
            pipeline_run.error_count += 1
            self.db.commit()

            return handle_service_error(e, "Scraping pipeline failed")
            
    async def _execute_scraping(self, pipeline_run_id: int, urls: List[str]) -> Dict[str, Any]:
        all_jobs = []
        total_scraped = 0
        total_processed = 0
        
        for provider_name, provider in self.providers.items():
            if not provider.is_active:
                continue
            
            session = ScrapingSession(
                pipeline_run_id=pipeline_run_id,
                site_name=provider_name,
                status="running",
                started_at=datetime.now()
            )
            self.db.add(session)
            self.db.commit()
            
            try:
                logger.info(f"Starting scraping with provider: {provider_name}")
                
                supported_sites = await provider.get_supported_sites()
                provider_urls = [
                    url for url in urls
                    if any(site in url for site in supported_sites)
                ]
                
                if not provider_urls:
                    logger.info(f"No URLs found for provider {provider_name}")
                    session.status = "completed"
                    session.completed_at = datetime.now()
                    self.db.commit()
                    continue
                
                jobs = await provider.scrape_jobs(provider_urls)
                
                processed_count = await self._save_jobs(jobs)
                
                session.jobs_found = len(jobs)
                session.jobs_successful = processed_count
                session.status = "completed"
                session.completed_at = datetime.now()
                self.db.commit()
                
                all_jobs.extend(jobs)
                total_scraped += len(jobs)
                total_processed += processed_count
                
                logger.info(f"Completed scraping with provider: {provider_name}, found {len(jobs)} jobs")
            
            except Exception as e:
                session.status = "failed"
                session.completed_at = datetime.now()
                self.db.commit()
                
                logger.error(f"Error scraping with provider {provider_name}: {e}")
                continue
        
        return {
            "total_scraped": total_scraped,
            "total_processed": total_processed,
            "jobs": all_jobs
        }
        
    async def _save_jobs(self, jobs: List[Dict[str, Any]]) -> int:
        processed_count = 0
        
        for job_data in jobs:
            try:
                existing =self.db.query(JobPosting).filter(
                    JobPosting.source_url == job_data.get('source_url')
                ).first()
                
                if existing:
                    logger.info(f"Job already exists: {job_data.get('source_url')}")
                    continue
                
                job_posting = JobPosting(
                    source_url=job_data.get('source_url', ''),
                    source_site=job_data.get('provider', 'unknown'),
                    job_title=job_data.get('job_title'),
                    company_name=job_data.get('company_name'),
                    location=job_data.get('location'),
                    employment_type=job_data.get('employment_type'),
                    experience_level=job_data.get('experience_level'),
                    full_text=job_data.get('job_description'),
                    technical_skills=job_data.get('required_skills', []),
                    soft_skills=job_data.get('preferred_skills', []),
                    status="raw"
                )
                
                self.db.add(job_posting)
                processed_count += 1
            
            except Exception as e:
                logger.error(f"Error saving job posting: {e}")
                continue
        
        self.db.commit()
        return processed_count
    
    async def get_provider_status(self) -> Dict[str, Any]:
        status = {}
        
        for name, provider in self.providers.items():
            try:
                test_result = await provider.test_connection()
                status[name] = {
                    "active": provider.is_active,
                    "info": provider.get_info(),
                    "test": test_result
                }
                
            except Exception as e:
                status[name] = {
                    "active": False,
                    "error": str(e)
                }
        return status
            