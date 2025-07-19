from sqlalchemy.orm import Session
from ..db import models
from ..api.v1.schemas import jobs as job_schemas
from typing import List, Any
from sqlalchemy import case

def get_job_by_source_url(db: Session, url: str) -> models.JobPosting | None:
    return db.query(models.JobPosting).filter(models.JobPosting.source_url == url).first()

def get_job_by_id(db: Session, job_id: int) -> models.JobPosting | None:
    return db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()

def create_job_posting(db:Session, url: str, site: str) -> models.JobPosting:
    db_job = models.JobPosting(
        source_url=url,
        source_site=site,
        status='raw',
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs_by_status(db: Session, status: str) -> list[type[models.JobPosting]]:
    return db.query(models.JobPosting).filter(models.JobPosting.status == status).all()

def update_job_with_enrichment_data(
        db: Session,
        job_id: int,
        details: job_schemas.JobDetails,
        embedding: List[float],
        full_text: str,
) -> models.JobPosting:
    db_job = get_job_by_id(db, job_id)

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

def update_job_status(db: Session, job_id: int, status: str) -> models.JobPosting:
    db_job = get_job_by_id(db, job_id=job_id)
    if db_job:
        db_job.status = status
        db.commit()
        db.refresh(db_job)
    return db_job

def get_matched_jobs_by_ids(db: Session, job_ids: List[int]) -> list[Any] | list[type[models.JobPosting]]:
    if not job_ids:
        return []

    ordering = case({id: index for index, job_id in enumerate(job_ids)}, value=models.JobPosting.id)

    return db.query(models.JobPosting).filter(models.JobPosting.id.in_(job_ids)).order_by(ordering).all()
