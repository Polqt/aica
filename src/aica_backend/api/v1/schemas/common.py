from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int

# Common filter models
class DateFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 50

# Health check models
class HealthStatus(BaseModel):
    status: str
    environment: str
    version: str
    features: Dict[str, bool]
    timestamp: datetime
    database_status: str
    redis_status: Optional[str] = None
    ai_services_status: Dict[str, str]

# API Key models
class APIKeyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    expires_at: Optional[datetime] = None

class APIKey(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool

# Skill models (common across features)
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class Skill(SkillBase):
    id: int
    class Config:
        from_attributes = True

class SkillWithProficiency(Skill):
    proficiency_level: Optional[str] = None  # beginner, intermediate, advanced, expert

# File upload models
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    content_type: str
    uploaded_at: datetime

# Search models
class SearchResult(BaseModel):
    item_id: int
    item_type: str  # "job", "profile", "skill"
    title: str
    description: Optional[str] = None
    relevance_score: float
    metadata: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    search_time: float
    filters_applied: Dict[str, Any]
