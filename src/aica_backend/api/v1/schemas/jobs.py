from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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