import logging

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_

from ..ai.pipeline.rag_pipeline import RAGPipeline
from ..core.config import settings
from ..database.models import User, UserProfile, JobPosting

logger = logging.getLogger(__name__)

class JobMatchingService:
    def __init__(self):
        self.rag_pipeline = RAGPipeline
        self._cache = {}
        self._cache_ttle = timedelta(minutes=30)
    
    async def get_job_matches_for_user(self,
                                       session: AsyncSession,
                                       user_id: int,
                                       filters: Optional[Dict[str, Any]] = None,
                                       limit: int = 20,
                                       use_cache: bool = True) -> Dict[str, Any]:
        
        try:
            # Check cache
            cache_key: f"job_matches_{user_id}_{hash(str(filters))}_{limit}"
            if use_cache and self._is_cache_valid(cache_key):
                logger.info(f"Returning cached results for user {user_id}")
                return self._cache[cache_key]['data']
            
            # Get user profile and skills
            user_profile = await self._get_user_profile(session, user_id)
            if not user_profile:
                return {
                    "error": "User profile not found",
                    "matches": [],
                    "total_matches": 0
                }
            
            user_skills = user_profile.get('skills', [])
            if not user_skills:
                return {
                    "error": "User skills not found",
                    "matches": [],
                    "total_matches": 0,
                    "suggestion": "Please add skills to your profile to get job recommendations"
                }
                
            # Applying business logic to filters
            enhanced_filters = self._enhance_filters_with_business_logic(
                filters or {},
                user_profile
            )
            
            rag_results = await self.rag_pipeline.find_matching_jobs(
                session=session,
                user_id=user_id,
                user_skills=user_skills,
                filters=enhanced_filters,
                limit=limit,
                generate_explanation=True
            )
            
            # Apply business enhancements
            enhanced_results = await self._enhance_results_with_business_data(
                session,
                rag_results,
                user_profile
            )
            
            # Cache results
            if use_cache:
                self._cache[cache_key] = {
                    'data': enhanced_results,
                    'timestamp': datetime.now()
                }
            
            await self._record_job_search_interaction(
                session,
                user_id,
                len(enhanced_results['matches'], filters)
            )
            
            return enhanced_results
            
            # Record user interaction
        except Exception as e:
            logger.error(f"Error occurred while getting job matches for user {user_id}: {e}")
            return {
                "error": str(e),
                "matches": [],
                "total_matches": 0
            }
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        if cache_key not in self._cache:
            return False
        
        cached_time = self._cache[cache_key]['timestamp']
        return datetime.now() - cached_time < self._cache_ttle