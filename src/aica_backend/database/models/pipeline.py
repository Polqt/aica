import datetime

from sqlalchemy import String, DateTime, Date, Text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base_class import Base
from typing import List, Optional

class PipelineRun(Base):
    __tablename__ = "pipeline_runs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    run_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="running", nullable=False)
    
    total_jobs_scraped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_jobs_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_jobs_embedded: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    
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
    
    jobs_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    jobs_successful: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    jobs_failed_scraping: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    pipeline_run: Mapped["PipelineRun"] = relationship(back_populates="scraping_sessions")
    
class ProcessingError(Base):
    __tablename__ = "processing_errors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    job_posting_id: Mapped[Optional[int]] = mapped_column(ForeignKey("job_postings.id"), nullable=True)
    pipeline_run_id: Mapped[Optional[int]] = mapped_column(ForeignKey("pipeline_runs.id"), nullable=True)
    
    error_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    error_message: Mapped[str] = mapped_column(Text, nullable=False)
    stack_trace: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )

    job_posting: Mapped[Optional["JobPosting"]] = relationship()
    pipeline_run: Mapped[Optional["PipelineRun"]] = relationship(back_populates="processing_errors")