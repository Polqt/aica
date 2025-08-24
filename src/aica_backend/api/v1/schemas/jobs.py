from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class JobDetails(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    extracted_skills: Optional[List[str]] = None
    work_type: Optional[str] = None
    employment_type: Optional[str] = None
    benefits: Optional[List[str]] = None
    extraction_quality_score: Optional[float] = None

class Job(BaseModel):
    id: int
    job_title: Optional[str] = None  
    company_name: Optional[str] = None 
    source_url: str
    source_site: str
    location: Optional[str] = None
    status: str = "raw"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes: True

class MatchedJobsResponse(BaseModel):
    matches: List[Job]

class ExplanationResponse(BaseModel):
    explanation: str

# Extended schemas for enhanced functionality
class JobCreate(BaseModel):
    source_url: str
    source_site: str
    external_id: Optional[str] = None
    full_text: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    work_type: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None

class JobUpdate(BaseModel):
    technical_skills: Optional[List[str]] = None
    soft_skills: Optional[List[str]] = None
    all_skills: Optional[List[str]] = None
    skill_categories: Optional[Dict[str, Any]] = None
    benefits: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    posting_date: Optional[datetime] = None
    application_deadline: Optional[date] = None
    extraction_quality_score: Optional[float] = None
    status: Optional[str] = None

class JobSearch(BaseModel):
    query: str
    location: Optional[str] = None
    work_type: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    skills: Optional[List[str]] = None

class JobStatistics(BaseModel):
    total_jobs: int
    jobs_by_status: Dict[str, int]
    jobs_by_site: Dict[str, int]
    jobs_by_work_type: Dict[str, int]
    jobs_by_experience_level: Dict[str, int]
    avg_extraction_quality: Optional[float] = None
    last_updated: datetime