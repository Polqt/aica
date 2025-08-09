from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class PipelineRunBase(BaseModel):
    status: str
    total_jobs_scraped: int = 0
    total_jobs_processed: int = 0
    total_jobs_embedded: int = 0
    error_count: int = 0

class PipelineRun(PipelineRunBase):
    id: int
    run_date: date
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PipelineRunResponse(BaseModel):
    id: int
    status: str
    started_at: datetime
    message: str

class PipelineRunDetail(PipelineRun):
    scraping_sessions: List['ScrapingSession']
    processing_errors: List['ProcessingError']

class ScrapingSession(BaseModel):
    id: int
    pipeline_run_id: int
    site_name: str
    jobs_found: int = 0
    jobs_successful: int = 0
    jobs_failed_scraping: int = 0
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProcessingError(BaseModel):
    id: int
    job_posting_id: Optional[int] = None
    pipeline_run_id: Optional[int] = None
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    retry_count: int = 0
    resolved: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class ProcessingResponse(BaseModel):
    processing_id: str
    message: str

class PipelineStatistics(BaseModel):
    total_runs: int
    successful_runs: int
    failed_runs: int
    running_runs: int
    total_jobs_scraped: int
    total_jobs_processed: int
    total_jobs_embedded: int
    total_errors: int
    avg_jobs_per_run: float
    last_run_date: Optional[datetime] = None

class JobProcessingStatus(BaseModel):
    total_jobs: int
    raw_jobs: int
    processed_jobs: int
    embedded_jobs: int
    failed_jobs: int
    processing_progress: float
