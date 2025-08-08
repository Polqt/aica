from sqlalchemy import String, DateTime, Date, Text, ForeignKey, Boolean, JSON, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from .base_class import Base
import datetime
from typing import List, Dict, Any, Optional

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )

    profile: Mapped[Optional["Profile"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan", 
        uselist=False
    )

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)

    # Personal Information
    first_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    professional_title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    contact_number: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(500), nullable=False)

    # Timestamps
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, 
        default=datetime.datetime.now, 
        onupdate=datetime.datetime.now
    )

    user: Mapped["User"] = relationship(back_populates="profile")
    educations: Mapped[List["Education"]] = relationship(
        cascade="all, delete-orphan", 
        back_populates="profile"
    )
    experiences: Mapped[List["Experience"]] = relationship(
        cascade="all, delete-orphan", 
        back_populates="profile"
    )
    certificates: Mapped[List["Certificate"]] = relationship(
        cascade="all, delete-orphan", 
        back_populates="profile"
    )
    skills: Mapped[List["Skill"]] = relationship(
        secondary="profile_skill_link", 
        back_populates="profiles"
    )

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    institution_name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    degree: Mapped[str] = mapped_column(String(100), nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="educations")

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    job_title: Mapped[str] = mapped_column(String(200), nullable=False)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="experiences")

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)

    profiles: Mapped[List["Profile"]] = relationship(
        secondary="profile_skill_link", 
        back_populates="skills"
    )


class ProfileSkillLink(Base):
    __tablename__ = "profile_skill_link"

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)
    proficiency_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # beginner, intermediate, advanced, expert

class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    issuing_organization: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    issue_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    credential_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    credential_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="certificates")

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
    
    # Additional job details
    benefits: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    requirements: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    
    # Dates
    posting_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    application_deadline: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    
    # AI/ML fields
    embedding: Mapped[Optional[Vector]] = mapped_column(Vector(768), nullable=True)
    extraction_quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Status and processing
    status: Mapped[str] = mapped_column(String(20), default="raw", index=True, nullable=False)  # raw, processed, embedded, failed
    
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
    
class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    run_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="running", nullable=False)
    
    # Metrics
    total_jobs_scraped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_jobs_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_jobs_embedded: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Timing
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    scraping_sessions: Mapped[List["ScrapingSession"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="pipeline_run"
    )
    processing_errors: Mapped[List["ProcessingError"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="pipeline_run"
    )

class ScrapingSession(Base):
    __tablename__ = "scraping_sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    pipeline_run_id: Mapped[int] = mapped_column(ForeignKey("pipeline_runs.id"), nullable=False)
    site_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    
    # Metrics
    jobs_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    jobs_successful: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    jobs_failed_scraping: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Status tracking
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    pipeline_run: Mapped["PipelineRun"] = relationship(back_populates="scraping_sessions")
    
class ProcessingError(Base):
    __tablename__ = "processing_errors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    job_posting_id: Mapped[Optional[int]] = mapped_column(ForeignKey("job_postings.id"), nullable=True)
    pipeline_run_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pipeline_runs.id"), nullable=True)
    
    # Error details
    error_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=False)
    stack_trace: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Retry information
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Timestamp
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )

    job_posting: Mapped[Optional["JobPosting"]] = relationship()
    pipeline_run: Mapped[Optional["PipelineRun"]] = relationship(back_populates="processing_errors")
    