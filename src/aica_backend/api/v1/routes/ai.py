"""
AI/RAG API endpoints - Simple version without pipeline service
Following REST principles and Clean Code
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ....services.matching_service import get_matching_service
from ....ai.rag.service import get_rag_service
from ....database.models import JobPosting, User
from ... import dependencies

router = APIRouter(prefix="/ai", tags=["AI/RAG"])

# Request/Response models
class CareerAdviceRequest(BaseModel):
    target_roles: Optional[List[str]] = None

class SkillGapRequest(BaseModel):
    job_id: int

class SimilarJobsRequest(BaseModel):
    query: str
    limit: int = 5

class MatchRequest(BaseModel):
    top_k: int = 10

@router.get("/status")
async def get_ai_status(
    current_user: dict = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    """Get current AI system status"""
    try:
        rag_service = get_rag_service()
        job_count = db.query(JobPosting).count()
        user_count = db.query(User).count()
        
        return {
            "rag_available": rag_service.llm is not None,
            "job_count": job_count,
            "user_count": user_count,
            "matching_service": "available",
            "status": "ready"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status check failed: {str(e)}"
        )

@router.post("/matches")
async def find_job_matches(
    request: MatchRequest,
    current_user: dict = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    """
    Find AI-powered job matches for current user
    Returns matches with basic insights
    """
    try:
        matching_service = get_matching_service()
        user_id = current_user["user_id"]
        
        # Get user and jobs
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        jobs = db.query(JobPosting).limit(50).all()  # Limit for performance
        
        # Convert to dictionaries
        user_profile = {
            "id": user.id,
            "email": user.email,
            "skills": [{"name": "Python"}, {"name": "JavaScript"}],  # Dummy for now
            "location": "Manila, Philippines",
            "work_preferences": {"work_types": ["Remote", "Hybrid"]}
        }
        
        job_dicts = []
        for job in jobs:
            job_dict = {
                "id": job.id,
                "job_title": job.job_title,
                "company_name": job.company_name,
                "location": job.location,
                "experience_level": job.experience_level,
                "work_type": job.work_type,
                "employment_type": job.employment_type,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "salary_currency": job.salary_currency,
                "full_text": job.full_text,
                "description": job.full_text,
                "requirements": job.requirements or []
            }
            job_dicts.append(job_dict)
        
        # Find matches
        matches = matching_service.find_matches(user_profile, job_dicts, request.top_k)
        
        # Convert to response format
        results = []
        for match in matches:
            job = next((j for j in jobs if j.id == match.job_id), None)
            if job:
                results.append({
                    "job": {
                        "id": job.id,
                        "job_title": job.job_title,
                        "company_name": job.company_name,
                        "location": job.location,
                        "work_type": job.work_type,
                        "salary_range": f"{job.salary_min}-{job.salary_max}" if job.salary_min else "Not specified"
                    },
                    "match_score": match.match_score,
                    "skill_match_percentage": match.skill_match_percentage,
                    "explanation": match.explanation,
                    "recommendations": match.recommendations
                })
        
        return {
            "matches": results,
            "total_found": len(results),
            "user_id": user_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Match finding failed: {str(e)}"
        )

@router.post("/similar-jobs")
async def find_similar_jobs(
    request: SimilarJobsRequest,
    current_user: dict = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    """
    Find similar jobs using semantic search
    """
    try:
        rag_service = get_rag_service()
        
        # For now, do a simple text search
        jobs = db.query(JobPosting).filter(
            JobPosting.full_text.ilike(f"%{request.query}%")
        ).limit(request.limit).all()
        
        results = []
        for job in jobs:
            results.append({
                "job": {
                    "id": job.id,
                    "job_title": job.job_title,
                    "company_name": job.company_name,
                    "location": job.location,
                    "work_type": job.work_type
                },
                "relevance_score": 0.8,  # Dummy score
                "matched_content": job.full_text[:200] + "..." if job.full_text else ""
            })
        
        return {
            "similar_jobs": results,
            "query": request.query,
            "total_found": len(results)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Similar job search failed: {str(e)}"
        )
