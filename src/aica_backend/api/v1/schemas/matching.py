from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from .jobs import Job

class JobMatch(BaseModel):
    job: Job
    match_score: float
    skill_match_score: float
    experience_match_score: float
    location_match_score: Optional[float] = None
    match_reasons: List[str]
    missing_skills: List[str]
    matching_skills: List[str]

class JobMatchResults(BaseModel):
    profile_id: int
    threshold: float
    total_matches: int
    matches: List[JobMatch]
    generated_at: datetime = datetime.now()

class ProfileMatch(BaseModel):
    job_id: int
    match_score: float
    compatibility_details: Dict[str, Any]
    recommendations: List[str]

class ProfileMatchResults(BaseModel):
    profile_id: int
    job_ids: List[int]
    matches: List[ProfileMatch]
    generated_at: datetime = datetime.now()

class SkillSuggestion(BaseModel):
    skill_name: str
    relevance_score: float
    job_demand: int
    market_trend: str  # "rising", "stable", "declining"
    related_skills: List[str]
    description: Optional[str] = None

class SkillSuggestionResponse(BaseModel):
    current_skills: List[str]
    suggestions: List[SkillSuggestion]
    market_insights: Dict[str, Any]

class CompatibilityAnalysis(BaseModel):
    overall_score: float
    skill_compatibility: Dict[str, Any]
    experience_compatibility: Dict[str, Any]
    education_compatibility: Dict[str, Any]
    location_compatibility: Optional[Dict[str, Any]] = None
    salary_compatibility: Optional[Dict[str, Any]] = None
    improvement_suggestions: List[str]
    strengths: List[str]
    gaps: List[str]
