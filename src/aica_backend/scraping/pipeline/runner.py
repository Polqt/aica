from typing import List, Optional
from sqlalchemy.orm import Session
from ...database.models import PipelineRun, ScrapingSession
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def start_pipeline(db: Session, sites: Optional[List[str]] = None) -> PipelineRun:
    """Start a new pipeline run"""
    try:
        pipeline_run = PipelineRun(
            status="running",
            started_at=datetime.now()
        )
        db.add(pipeline_run)
        db.commit()
        db.refresh(pipeline_run)
        
        logger.info(f"Started pipeline run {pipeline_run.id}")
        return pipeline_run
        
    except Exception as e:
        logger.error(f"Failed to start pipeline: {str(e)}")
        db.rollback()
        raise

def execute_pipeline(db: Session, pipeline_id: int):
    """Execute pipeline (placeholder for now)"""
    try:
        pipeline_run = db.query(PipelineRun).filter(PipelineRun.id == pipeline_id).first()
        if pipeline_run:
            pipeline_run.status = "completed"
            pipeline_run.completed_at = datetime.now()
            db.commit()
            logger.info(f"Completed pipeline run {pipeline_id}")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")

def stop_pipeline(db: Session, run_id: int) -> bool:
    """Stop a running pipeline"""
    try:
        pipeline_run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
        if pipeline_run:
            pipeline_run.status = "stopped"
            pipeline_run.completed_at = datetime.now()
            db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to stop pipeline: {str(e)}")
        return False

def start_job_processing(db: Session, force_reprocess: bool = False) -> str:
    """Start job processing (placeholder)"""
    return f"processing_{datetime.now().timestamp()}"

def execute_job_processing(db: Session, processing_id: str):
    """Execute job processing (placeholder)"""
    logger.info(f"Job processing {processing_id} completed")
