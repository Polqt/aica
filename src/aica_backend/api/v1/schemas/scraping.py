from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ScrapingProvider(BaseModel):
    name: str
    description: str
    supported_features: List[str]
    rate_limit: int
    status: str 

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

class ScrapingSessionDetail(ScrapingSession):
    error_logs: List['ScrapingError']
    performance_metrics: Dict[str, Any]

class ScrapingError(BaseModel):
    id: int
    session_id: Optional[int] = None
    provider_name: str
    error_type: str
    error_message: str
    url: Optional[str] = None
    retry_count: int = 0
    resolved: bool = False
    created_at: datetime
    stack_trace: Optional[str] = None

    class Config:
        from_attributes = True

class ScrapingConfig(BaseModel):
    providers: Dict[str, Dict[str, Any]]
    global_settings: Dict[str, Any]
    rate_limits: Dict[str, int]
    retry_settings: Dict[str, int]

class ProviderTestResult(BaseModel):
    provider: str
    test_url: str
    success: bool
    data: Dict[str, Any]
    errors: List[str]
    execution_time: float

class ScrapingStatistics(BaseModel):
    total_sessions: int
    successful_sessions: int
    failed_sessions: int
    total_jobs_scraped: int
    jobs_per_provider: Dict[str, int]
    avg_success_rate: float
    last_scraping_date: Optional[datetime] = None
