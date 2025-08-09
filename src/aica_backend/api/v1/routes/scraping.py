from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ....database import models
from ....scraping.providers import factory
from ....scraping.pipeline import monitor
from .. import schemas
from ... import dependencies

router = APIRouter()

@router.get("/providers", response_model=List[schemas.scraping.ScrapingProvider])
def get_scraping_providers():
    """Get list of available scraping providers"""
    providers = factory.get_available_providers()
    return [
        schemas.scraping.ScrapingProvider(
            name=name,
            description=info.get("description", ""),
            supported_features=info.get("features", []),
            rate_limit=info.get("rate_limit", 0),
            status="active" if info.get("active", True) else "inactive"
        )
        for name, info in providers.items()
    ]

@router.get("/providers/{provider_name}/test")
def test_scraping_provider(
    provider_name: str,
    test_url: Optional[str] = Query(None),
    db: Session = Depends(dependencies.get_db),
):
    """Test a specific scraping provider"""
    try:
        provider = factory.get_provider(provider_name)
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Use test URL or provider's default test URL
        url = test_url or provider.get_test_url()
        if not url:
            raise HTTPException(status_code=400, detail="No test URL provided")
        
        result = provider.test_scraping(url)
        return {
            "provider": provider_name,
            "test_url": url,
            "success": result.get("success", False),
            "data": result.get("data", {}),
            "errors": result.get("errors", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider test failed: {str(e)}")

@router.get("/sessions", response_model=List[schemas.scraping.ScrapingSession])
def get_scraping_sessions(
    provider: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(dependencies.get_db),
):
    """Get scraping session history"""
    filters = {}
    if provider:
        filters["site_name"] = provider
    if status:
        filters["status"] = status
        
    sessions = monitor.get_scraping_sessions(
        db=db, 
        skip=skip, 
        limit=limit, 
        filters=filters
    )
    return [schemas.scraping.ScrapingSession.model_validate(session) for session in sessions]

@router.get("/sessions/{session_id}", response_model=schemas.scraping.ScrapingSessionDetail)
def get_scraping_session(
    session_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """Get detailed information about a specific scraping session"""
    session_detail = monitor.get_scraping_session_detail(db=db, session_id=session_id)
    if not session_detail:
        raise HTTPException(status_code=404, detail="Scraping session not found")
    return session_detail

@router.get("/errors", response_model=List[schemas.scraping.ScrapingError])
def get_scraping_errors(
    provider: Optional[str] = Query(None),
    error_type: Optional[str] = Query(None),
    resolved: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(dependencies.get_db),
):
    """Get scraping errors for debugging"""
    filters = {}
    if provider:
        filters["provider"] = provider
    if error_type:
        filters["error_type"] = error_type
    if resolved is not None:
        filters["resolved"] = resolved
        
    errors = monitor.get_scraping_errors(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters
    )
    return [schemas.scraping.ScrapingError.model_validate(error) for error in errors]

@router.post("/errors/{error_id}/resolve")
def resolve_scraping_error(
    error_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """Mark a scraping error as resolved"""
    try:
        success = monitor.resolve_scraping_error(db=db, error_id=error_id)
        if not success:
            raise HTTPException(status_code=404, detail="Error not found")
        return {"message": "Error marked as resolved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resolve error: {str(e)}")

@router.get("/config")
def get_scraping_config():
    """Get current scraping configuration"""
    try:
        config = factory.get_scraping_config()
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get config: {str(e)}")

@router.put("/config")
def update_scraping_config(
    config: Dict[str, Any],
    db: Session = Depends(dependencies.get_db),
):
    """Update scraping configuration"""
    try:
        updated_config = factory.update_scraping_config(config)
        return {
            "message": "Configuration updated successfully",
            "config": updated_config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update config: {str(e)}")
