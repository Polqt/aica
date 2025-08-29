import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, String, DateTime, Date, Text, JSON, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from ..base_class import Base
from typing import List, Optional, Dict, Any

from ...core.config import settings

class JobPosting(Base):
    __tablename__ = "job_postings"

    # Primary identifiers
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_url: Mapped[str] = mapped_column(String(1000), unique=True, index=True, nullable=False)
    source_site: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)

    # Basic job information
    job_title: Mapped[Optional[str]] = mapped_column(String(200), index=True, nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(200), index=True, nullable=True)
    full_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Location information
    location: Mapped[Optional[str]] = mapped_column(String(200), index=True, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    
    # Job type and employment details
    work_type: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)  # remote, hybrid, onsite
    employment_type: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)  # full-time, part-time, contract
    experience_level: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)  # entry, mid, senior
    
    tech_category: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    
    # Salary information
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    salary_period: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # hourly, monthly, yearly
    
    # Extracted skills and requirements
    technical_skills: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    soft_skills: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    all_skills: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    skill_categories: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    requirements: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Additional job details
    benefits: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    requirements: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Dates
    posting_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    application_deadline: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    
    # AI/ML fields
    skills_embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(settings.EMBEDDING_DIMENSION), nullable=True)
    description_embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(settings.EMBEDDING_DIMENSION), nullable=True)
    
    extraction_quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Status and processing
    status: Mapped[str] = mapped_column(String(20), default="raw", index=True, nullable=False)  # raw, processed, embedded, failed
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now,
        nullable=False
    )
    