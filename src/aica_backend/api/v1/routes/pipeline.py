from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from ....database import models
from ....database.repositories import jobs
from ....scraping.pipeline import runner
from ....scraping.pipeline import monitor
from .. import schemas
from ... import dependencies

router = APIRouter()

@router.post("/scraping/start", response_model=schemas.pipeline.PipelineRunResponse)
def start_scraping_pipeline(
    background_tasks: BackgroundTasks,
    sites: Optional[List[str]] = None,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    try:
        pipeline_run = runner.start_pipeline(db=db, sites=sites)
        
        background_tasks.add_task(
            runner.execute_pipeline, 
            db, 
            pipeline_run.id
        )
        
        return schemas.pipeline.PipelineRunResponse(
            id=pipeline_run.id,
            status=pipeline_run.status,
            started_at=pipeline_run.started_at,
            message="Pipeline started successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start pipeline: {str(e)}")

@router.get("/runs", response_model=List[schemas.pipeline.PipelineRun])
def get_pipeline_runs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(dependencies.get_db),
):
    runs = monitor.get_pipeline_runs(db=db, skip=skip, limit=limit)
    return [schemas.pipeline.PipelineRun.model_validate(run) for run in runs]

@router.get("/runs/{run_id}", response_model=schemas.pipeline.PipelineRunDetail)
def get_pipeline_run(
    run_id: int,
    db: Session = Depends(dependencies.get_db),
):
    run_detail = monitor.get_pipeline_run_detail(db=db, run_id=run_id)
    if not run_detail:
        raise HTTPException(status_code=404, detail="Pipeline run not found")
    return run_detail

@router.post("/runs/{run_id}/stop")
def stop_pipeline_run(
    run_id: int,
    db: Session = Depends(dependencies.get_db),
):
    try:
        success = runner.stop_pipeline(db=db, run_id=run_id)
        if not success:
            raise HTTPException(status_code=404, detail="Pipeline run not found or not running")
        return {"message": "Pipeline stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop pipeline: {str(e)}")

@router.get("/stats/overview")
def get_pipeline_stats(db: Session = Depends(dependencies.get_db)):
    stats = monitor.get_pipeline_statistics(db=db)
    return stats

@router.post("/processing/start", response_model=schemas.pipeline.ProcessingResponse)
def start_job_processing(
    background_tasks: BackgroundTasks,
    force_reprocess: bool = False,
    db: Session = Depends(dependencies.get_db),
):
    try:
        processing_id = runner.start_job_processing(
            db=db, 
            force_reprocess=force_reprocess
        )
        
        # Run processing in background
        background_tasks.add_task(
            runner.execute_job_processing,
            db,
            processing_id
        )
        
        return schemas.pipeline.ProcessingResponse(
            processing_id=processing_id,
            message="Job processing started successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start processing: {str(e)}")

@router.get("/jobs/status")
def get_job_processing_status(db: Session = Depends(dependencies.get_db)):
    status = monitor.get_job_processing_status(db=db)
    return status
