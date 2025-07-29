from sqlalchemy import String, DateTime, Date, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from .base_class import Base
import datetime
from typing import List, Dict, Any

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

    profile: Mapped["Profile"] = relationship(back_populates="user", cascade="all, delete-orphan", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    first_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    professional_title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    contact_number: Mapped[str] = mapped_column(String, index=True, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    linkedin_url: Mapped[str] = mapped_column(String, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    profile_picture: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    educations: Mapped[List["Education"]] = relationship(cascade="all, delete-orphan")
    experiences: Mapped[List["Experience"]] = relationship(cascade="all, delete-orphan")
    certificates: Mapped[List["Certificate"]] = relationship(cascade="all, delete-orphan")
    skills: Mapped[List["Skill"]] = relationship(secondary="profile_skill_link", back_populates="profiles")

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    institution_name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    degree: Mapped[str] = mapped_column(String, nullable=False)
    field_of_study: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    job_title: Mapped[str] = mapped_column(String, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[List[str]] = mapped_column(JSON, nullable=True)

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    profiles: Mapped[List["Profile"]] = relationship(secondary="profile_skill_link", back_populates="skills")


class ProfileSkillLink(Base):
    __tablename__ = "profile_skill_link"

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=True)
    issuing_organization: Mapped[str] = mapped_column(String, nullable=True)
    issue_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    credential_url: Mapped[str] = mapped_column(String, nullable=True)
    credential_id: Mapped[str] = mapped_column(String, nullable=True)

class JobPosting(Base):
    __tablename__ = "job_postings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_url: Mapped[str] = mapped_column(String, unique=True, index=True)
    source_site: Mapped[str] = mapped_column(String, index=True)

    full_text: Mapped[str] = mapped_column(Text, nullable=True)

    job_title: Mapped[str] = mapped_column(String, nullable=True, index=True)
    company_name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    full_text: Mapped[str] = mapped_column(Text, nullable=True)
    
    location: Mapped[str] = mapped_column(String, nullable=True, index=True)
    country: Mapped[str] = mapped_column(String, nullable=True, index=True)
    work_type: Mapped[str] = mapped_column(String, nullable=True, index=True)  
    employment_type: Mapped[str] = mapped_column(String, nullable=True, index=True)
    
    salary_min: Mapped[int] = mapped_column(nullable=True)
    salary_max: Mapped[int] = mapped_column(nullable=True)
    salary_currency: Mapped[str] = mapped_column(String, nullable=True)
    salary_period: Mapped[str] = mapped_column(String, nullable=True)  
    experience_level: Mapped[str] = mapped_column(String, nullable=True, index=True)
    
    technical_skills: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    soft_skills: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    all_skills: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    skill_categories: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
    
    benefits: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    posting_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=True)
    status: Mapped[str] = mapped_column(String, default="raw", index=True)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    run_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    status: Mapped[str] = mapped_column(String, default="running")
    total_jobs_scraped: Mapped[int] = mapped_column(default=0)
    total_jobs_processed: Mapped[int] = mapped_column(default=0)
    total_jobs_embedded: Mapped[int] = mapped_column(default=0)
    error_count: Mapped[int] = mapped_column(default=0)
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

class ScrapingSession(Base):
    __tablename__ = "scraping_sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    pipeline_run_id: Mapped[int] = mapped_column(ForeignKey("pipeline_runs.id"))
    site_name: Mapped[str] = mapped_column(String, index=True)
    jobs_found: Mapped[int] = mapped_column(default=0)
    jobs_successful: Mapped[int] = mapped_column(default=0)
    jobs_failed_scraping: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String, default="pending")
    
class ProcessingError(Base):
    __tablename__ = "processing_errors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    job_posting_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id"), nullable=True)
    pipeline_run_id: Mapped[int] = mapped_column(ForeignKey("pipeline_runs.id"), nullable=True)
    error_type: Mapped[str] = mapped_column(String, index=True)
    error_message: Mapped[str] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    