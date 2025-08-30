from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any
from ... import dependencies
from ....database import models
from ....rag.embeddings.embedding_service import embedding_service
from ....rag.embeddings.store_factory import get_vector_store

router = APIRouter()

@router.get("/recommendations")
def get_recommendations(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
) -> Dict[str, Any]:
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    user_skills = [s.name for s in (current_user.profile.skills or [])]
    if not user_skills:
        return {"matches": [], "total_matches": 0}

    try:
        user_emb = embedding_service.encode_skills(user_skills)
        vs = get_vector_store()
        matches = vs.find_similar_jobs_sync(db, user_emb, limit=limit)
        return {"matches": matches, "total_matches": len(matches)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {str(e)}")
