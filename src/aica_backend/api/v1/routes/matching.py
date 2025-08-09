from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....database import models
from ....services import matching
from ..schemas import matching as matching_schemas
from ... import dependencies

router = APIRouter()

@router.post("/profile-to-jobs", response_model=matching_schemas.JobMatchResults)
def match_profile_to_jobs(
    limit: int = Query(50, ge=1, le=200),
    threshold: float = Query(0.7, ge=0.1, le=1.0),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """Match current user's profile to available jobs"""
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    try:
        results = matching.match_profile_to_jobs(
            db=db,
            profile=current_user.profile,
            limit=limit,
            threshold=threshold
        )
        return matching_schemas.JobMatchResults(
            profile_id=current_user.profile.id,
            threshold=threshold,
            total_matches=len(results),
            matches=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

@router.post("/jobs-to-profile", response_model=matching_schemas.ProfileMatchResults)
def match_jobs_to_profile(
    job_ids: List[int],
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """Match specific jobs to current user's profile"""
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    try:
        results = matching.match_jobs_to_profile(
            db=db,
            profile=current_user.profile,
            job_ids=job_ids
        )
        return matching_schemas.ProfileMatchResults(
            profile_id=current_user.profile.id,
            job_ids=job_ids,
            matches=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

@router.get("/skills/suggestions")
def get_skill_suggestions(
    current_skills: List[str] = Query(...),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(dependencies.get_db),
):
    """Get skill suggestions based on current skills and job market"""
    try:
        suggestions = matching.get_skill_suggestions(
            db=db,
            current_skills=current_skills,
            limit=limit
        )
        return {
            "current_skills": current_skills,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill suggestion failed: {str(e)}")

@router.get("/profile/{profile_id}/compatibility")
def get_profile_job_compatibility(
    profile_id: int,
    job_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """Get detailed compatibility analysis between a profile and job"""
    # Check if user owns the profile or is admin
    if current_user.profile.id != profile_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        compatibility = matching.analyze_compatibility(
            db=db,
            profile_id=profile_id,
            job_id=job_id
        )
        return compatibility
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compatibility analysis failed: {str(e)}")
