from pydantic import BaseModel
from typing import List, Optional

class JobDetails(BaseModel):
    job_title: str
    company_name: str
    extracted_skills: List[str]

class Job(BaseModel):
    id: int
    job_title: str
    company_name: str
    source_url: str
    source_site: str

    class Config:
        from_attributes: True

class MatchedJobsResponse(BaseModel):
    matches: List[Job]

class ExplanationResponse(BaseModel):
    explanation: str