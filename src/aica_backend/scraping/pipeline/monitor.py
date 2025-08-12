from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ...database.models import PipelineRun, ScrapingSession, ProcessingError
import logging

logger = logging.getLogger(__name__)

def get_pipeline_runs(db: Session, skip: int = 0, limit: int = 50) -> List[PipelineRun]:
    return db.query(PipelineRun).offset(skip).limit(limit).all()

def get_pipeline_run_detail(db: Session, run_id: int) -> Optional[PipelineRun]:
    return db.query(PipelineRun).filter(PipelineRun.id == run_id).first()

def get_pipeline_statistics(db: Session) -> Dict[str, Any]:
    total_runs = db.query(PipelineRun).count()
    running_runs = db.query(PipelineRun).filter(PipelineRun.status == "running").count()
    completed_runs = db.query(PipelineRun).filter(PipelineRun.status == "completed").count()
    failed_runs = db.query(PipelineRun).filter(PipelineRun.status == "failed").count()
    
    return {
        "total_runs": total_runs,
        "successful_runs": completed_runs,
        "failed_runs": failed_runs,
        "running_runs": running_runs,
        "total_jobs_scraped": 0, 
        "total_jobs_processed": 0, 
        "total_jobs_embedded": 0,
        "total_errors": 0, 
        "avg_jobs_per_run": 0.0,  
        "last_run_date": None  
    }

def get_scraping_sessions(db: Session, skip: int = 0, limit: int = 50, filters: Dict = None) -> List[ScrapingSession]:
    query = db.query(ScrapingSession)
    
    if filters:
        if "site_name" in filters:
            query = query.filter(ScrapingSession.site_name == filters["site_name"])
        if "status" in filters:
            query = query.filter(ScrapingSession.status == filters["status"])
    
    return query.offset(skip).limit(limit).all()

def get_scraping_session_detail(db: Session, session_id: int) -> Optional[Dict[str, Any]]:
    session = db.query(ScrapingSession).filter(ScrapingSession.id == session_id).first()
    if not session:
        return None
    
    return {
        "id": session.id,
        "pipeline_run_id": session.pipeline_run_id,
        "site_name": session.site_name,
        "jobs_found": session.jobs_found,
        "jobs_successful": session.jobs_successful,
        "jobs_failed_scraping": session.jobs_failed_scraping,
        "status": session.status,
        "started_at": session.started_at,
        "completed_at": session.completed_at,
        "error_logs": [],  # Placeholder
        "performance_metrics": {}  # Placeholder
    }

def get_scraping_errors(db: Session, skip: int = 0, limit: int = 50, filters: Dict = None) -> List[ProcessingError]:
    query = db.query(ProcessingError)
    
    if filters:
        if "provider" in filters:
            query = query.filter(ProcessingError.error_type.contains(filters["provider"]))
        if "error_type" in filters:
            query = query.filter(ProcessingError.error_type == filters["error_type"])
        if "resolved" in filters:
            query = query.filter(ProcessingError.resolved == filters["resolved"])
    
    return query.offset(skip).limit(limit).all()

def resolve_scraping_error(db: Session, error_id: int) -> bool:
    try:
        error = db.query(ProcessingError).filter(ProcessingError.id == error_id).first()
        if error:
            error.resolved = True
            db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to resolve error: {str(e)}")
        return False

def get_job_processing_status(db: Session) -> Dict[str, Any]:
    return {
        "total_jobs": 0,
        "raw_jobs": 0,
        "processed_jobs": 0,
        "embedded_jobs": 0,
        "failed_jobs": 0,
        "processing_progress": 0.0
    }
