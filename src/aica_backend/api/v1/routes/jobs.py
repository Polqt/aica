from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ....database.repositories import jobs
from ....services import job_management
from .. import schemas
from ... import dependencies

router = APIRouter()


@router.get("/", response_model=List[schemas.jobs.Job])
def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    location: Optional[str] = Query(None),
    work_type: Optional[str] = Query(None),
    employment_type: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    salary_min: Optional[int] = Query(None),
    salary_max: Optional[int] = Query(None),
    db: Session = Depends(dependencies.get_db),
):
    """Get jobs with optional filtering."""
    filters = {
        k: v for k, v in {
            "location": location,
            "work_type": work_type,
            "employment_type": employment_type,
            "experience_level": experience_level,
            "salary_min": salary_min,
            "salary_max": salary_max,
        }.items() if v is not None
    }
    
    job_list = jobs.get_jobs(db=db, skip=skip, limit=limit, filters=filters)
    return [schemas.jobs.Job.model_validate(job) for job in job_list]


@router.get("/{job_id}", response_model=schemas.jobs.Job)
def get_job(
    job_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """Get job by ID."""
    job = jobs.get_job(db=db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

@router.get("/search/by-skills")
def search_jobs_by_skills(
    skills: List[str] = Query(...),
    limit: int = Query(50, ge=1, le=200),
    threshold: float = Query(0.7, ge=0.1, le=1.0),
    db: Session = Depends(dependencies.get_db),
):
    try:
        results = job_management.search_jobs_by_skills(
            db=db,
            skills=skills,
            limit=limit,
            threshold=threshold
        )
        return {
            "query_skills": skills,
            "threshold": threshold,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/stats/overview")
def get_job_stats(db: Session = Depends(dependencies.get_db)):
    stats = jobs.get_job_statistics(db=db)
    return stats
