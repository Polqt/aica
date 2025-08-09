from sqlalchemy import case
from sqlalchemy.orm import Session
from typing import List, Optional, Any

from .base import BaseCRUD
from .. import models
from ...api.v1.schemas import jobs as job_schemas

JobPosting = models.JobPosting

class JobCRUD(BaseCRUD[JobPosting, job_schemas.JobCreate, job_schemas.JobUpdate]):
    def get_job_by_source_url(self, db: Session, url: str) -> Optional[models.JobPosting]:
        return db.query(models.JobPosting).filter(
            models.JobPosting.source_url == url
        ).first()

    def get_job_by_id(self, db: Session, job_id: int) -> Optional[models.JobPosting]:
        return db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()

    def create_job_posting(self, db: Session, url: str, site: str) -> models.JobPosting:
        db_job = models.JobPosting(
            source_url=url,
            source_site=site,
            status='raw',
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    
    # Prevent duplicate for scraping
    def get_or_create_job(self, db: Session, url: str, site: str) -> tuple[models.JobPosting, bool]:
        existing_job = self.get_job_by_source_url(db, url)
        if existing_job:
            return existing_job, False
        return self.create_job_posting(db, url, site), True

    def get_jobs_by_status(self, db: Session, status: str) -> List[models.JobPosting]:
        return db.query(models.JobPosting).filter(models.JobPosting.status == status).all()

    # For LLM extraction
    def update_job_with_enrichment_data(
            self,
            db: Session,
            job_id: int,
            details: job_schemas.JobDetails,
            embedding: List[float],
            full_text: str,
    ) -> Optional[models.JobPosting]:
        db_job = self.get_job_by_id(db, job_id)

        if db_job:
            db_job.job_title = details.job_title
            db_job.company_name = details.company_name
            db_job.extracted_skills = details.extracted_skills
            db_job.full_text = full_text
            db_job.embedding = embedding
            db_job.status = 'embedded'
            db.commit()
            db.refresh(db_job)
        return db_job

    def update_job_status(self, db: Session, job_id: int, status: str) -> Optional[models.JobPosting]:
        db_job = self.get_job_by_id(db, job_id)
        if db_job:
            db_job.status = status
            db.commit()
            db.refresh(db_job)
        return db_job

    def get_matched_jobs_by_ids(self, db: Session, job_ids: List[int]) -> List[models.JobPosting]:
        if not job_ids:
            return []

        ordering = case({job_id: index for index, job_id in enumerate(job_ids)}, value=models.JobPosting.id)
        return db.query(models.JobPosting).filter(models.JobPosting.id.in_(job_ids)).order_by(ordering).all()

crud_jobs = JobCRUD(models.JobPosting)