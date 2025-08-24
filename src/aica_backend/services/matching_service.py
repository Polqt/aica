import logging

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_

from ai.pipeline.rag_pipeline import rag_pipeline
from ..core.config import settings
from ..database.models import User, UserProfile, JobPosting

logger = logging.getLogger(__name__)

class JobMatchingService:
    def __init__(self):
        self.rag_pipeline = rag_pipeline
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
    
    async def get_detailed_job_analysis(self,
                                        session: AsyncSession,
                                        user_id: int,
                                        job_id: int) -> Dict[str, Any]:
        """
            Get detailed compatibility analysis for a specific job.
        """
        
        try:
            # Get user profile
            user_profile = await self._get_user_profile(session, user_id)
            if not user_profile:
                return {
                    "error": "User profile not found",
                    "analysis": {}
                }
            
            user_skills = user_profile.get('skills', [])
            
            # Get compatibility analysis from RAG pipeline
            analysis = await self.rag_pipeline.analyze_job_compatibility(
                session,
                user_skills,
                job_id
            )
            
            if 'error' in analysis:
                return analysis
            
            # Enhance with business insights
            enhanced_analysis = await self._enhance_job_analysis(
                session,
                analysis,
                user_profile
            )
            
            await self._record_job_view_interaction(
                session,
                user_id,
                job_id
            )
            
            return enhanced_analysis
        except Exception as e:
            logger.error(f"Error occurred while getting detailed job analysis for user {user_id} and job {job_id}: {e}")
            return {
                "error": str(e),
                "analysis": {}
            }
    
    async def get_career_dashboard(self,
                                   session: AsyncSession,
                                   user_id: int) -> Dict[str, Any]:
        """
            Generate comprehensive career dashboard for user
        """
        
        try:
            # Get user profile
            user_profile = await self._get_user_profile(session, user_id)
            if not user_profile:
                return {
                    "error": "User profile not found",
                    "dashboard": {}
                }

            # Get recent job matches for context
            recent_matches = await self.get_job_matches_for_user(
                session,
                user_id,
                limit=10,
                use_cache=False
            )
            
            # Generate career insights 
            career_insights = await self.rag_pipeline.generate_career_insights(
                session,
                user_profile,
                recent_matches.get('matches', [])
            )
            
            # Get user statistics
            user_stats = await self._get_user_statistics(session, user_id)
            
            # Get skill trends
            skill_trends = await self._get_skill_market_trends(
                session,
                user_profile.get('skills', [])
            )
            
            dashboard = {
                "user_profile": user_profile,
                "career_insights": career_insights,
                "recent_matches": {
                    "total": recent_matches.get('total_matches', 0),
                    "top_matches": recent_matches.get('matches', [])[:5]
                },
                "user_statistics": user_stats,
                "skill_market_trends": skill_trends,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            return dashboard
        except Exception as e:
            logger.error(f"Error generating career dashboard for user {user_id}: {str(e)}")
            return {"error": str(e)}
        
    async def batch_process_new_jobs(self,
                                    session: AsyncSession,
                                    job_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
            Process a batch of new jobs for embedding generation.
        """
        
        try:
            # Processing embeddings
            processing_result = await self.rag_pipeline.process_job_batch_for_embedding(
                session,
                job_batch
            )
            
            # Clear relevant caches since new jobs are available
            self._clear_all_user_caches()
            
            # Update job processing stats
            await self._update_job_processing_stats(session, processing_result)
            
            return {
                **processing_result,
                "cached_cleared": True,
                "processed_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error batch processing jobs: {str(e)}")
            return {"error": str(e)}
        
    async def _get_user_profile(self, session: AsyncSession, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = text("""
                         SELECT
                            up.user_id,
                            up.full_name,
                            up.title,
                            up.skills,
                            up.experience_years,
                            up.location,
                            up.preferred_job_types,
                            up.preferred_locations,
                            up.salary_expectations,
                            up.work_style_preferences,
                            u.email
                        FROM user_profile AS up
                        JOIN users AS u 
                            ON u.id = up.user_id
                        WHERE up.user_id = :user_id AND up.is_active = true
                        """)
            
            result = await session.execute(query, {'user_id': user_id})
            row = result.fetchone()
            
            if not row:
                return None
            
            return {
                'user_id': row.user_id,
                'full_name': row.full_name,
                'title': row.title,
                'skills': row.skills or [],
                'experience_years': row.experience_years,
                'location': row.location,
                'preferred_job_types': row.preferred_job_types or [],
                'preferred_locations': row.preferred_locations or [],
                'salary_expectations': row.salary_expectations,
                'work_style_preferences': row.work_style_preferences,
                'email': row.email
            }
        except Exception as e:
            logger.error(f"Error fetching user profile for user {user_id}: {e}")
            return None
        
    def _enhance_filters_with_business_logic(self,
                                            filters: Dict[str, Any],
                                            user_profile: Dict[str, Any]) -> Dict[str, Any]:
        
        enhanced_filters = filters.copy()
        
        # Add user preferences if not specified
        if not enhanced_filters.get('location') and user_profile.get('preferred_locations'):
            enhanced_filters['preferred_locations'] = user_profile['preferred_locations']
        
        if not enhanced_filters.get('job_type') and user_profile.get('preferred_job_types'):
            enhanced_filters['preferred_job_types'] = user_profile['preferred_job_types']
            
        # Add salary expectations
        if user_profile.get('salary_expectations'):
            if not enhanced_filters.get('min_salary'):
                enhanced_filters['min_salary'] = user_profile['salary_expectations'].get('min')
            if not enhanced_filters.get('max_salary'):
                enhanced_filters['max_salary'] = user_profile['salary_expectations'].get('max')
            
        # Experience level matching
        experience_years = user_profile.get('experience_years', 0)
        if not enhanced_filters.get('experience_level'):
            if experience_years < 2:
                enhanced_filters['experience_level'] = ['Entry Level', 'Junior']
            elif experience_years < 5:
                enhanced_filters['experience_level'] = ['Mid Level', 'Intermediate']
            else:
                enhanced_filters['experience_level'] = ['Senior', 'Lead', 'Principal']
        
        return enhanced_filters
    
    async def _enhance_results_with_business_data(self,
                                                  session: AsyncSession,
                                                  rag_results: Dict[str, Any],
                                                  user_profile: Dict[str, Any]) -> Dict[str, Any]:
        
        enhanced_results = rag_results.copy()
        
        for match in enhanced_results.get('matches', []):
            # Calculate business match score
            business_score = self._calculate_business_match_score(match, user_profile)
            match['business_match_score'] = business_score
            
            # Application difficulty estimate
            match['application_difficulty'] = self._estimate_application_difficulty(
                match,
                user_profile
            )
            
            # Estimated response time
            match['estimated_response_time'] = self._estimated_response_time(match)
            
            # Company insights
            company_insights = await self._get_company_insights(session, match['company_name'])
            if company_insights:
                match['company_insights'] = company_insights
        
        # Sort it using combined score
        enhanced_results['matches'].sort(
            key=lambda x: (
                x.get('similarity_scores', {}).get('combined_similarity', 0) * 0.6 +
                x.get('business_match_score', 0) * 0.4
            ),
            reverse=True
        )
        
        return enhanced_results
    
    def _calculate_business_match_score(self,
                                        job_match: Dict[str, Any],
                                        user_profile: Dict[str, Any]) -> float:
        
        score = 0.0
        
        # Location preference match
        user_locations = user_profile.get('preferred_locations', [])
        job_location = job_match.get('location', '')
        if any(loc.lower() in job_location.lower() for loc in user_locations):
            score += 0.2
        
        # Job type preference match
        user_job_types = user_profile.get('preferred_job_types', [])
        job_type = job_match.get('job_type', '')
        if job_type in user_job_types:
            score += 0.2
        
        # Experience level alignment
        user_experience = user_profile.get('experience_years', 0)
        job_experience_level = job_match.get('experience_level', '').lower()
        
        if user_experience < 2 and any(level in job_experience_level for level in ['entry', 'junior']):
            score += 0.2
        elif 2 <= user_experience < 5 and any(level in job_experience_level for level in ['mid', 'intermediate']):
            score += 0.2
        elif user_experience >= 5 and any(level in job_experience_level for level in ['senior', 'lead']):
            score += 0.2
        
        # Salary expectations alignment
        salary_expectations = user_profile.get('salary_expectations', {})
        job_salary_min = job_match.get('salary_min')
        if salary_expectations.get('min') and job_salary_min:
            if job_salary_min >= salary_expectations['min'] * 0.8:  # Within 20% tolerance
                score += 0.2
        
        # Recent posting bonus (shows active hiring)
        posted_date = job_match.get('posted_date')
        if posted_date and isinstance(posted_date, datetime):
            days_since_posted = (datetime.utcnow() - posted_date).days
            if days_since_posted <= 7:
                score += 0.2
        
        return min(score, 1.0)

    def _estimate_response_time(self, job_match: Dict[str, Any]) -> str:
        posted_date = job_match.get('posted_date')
        if posted_date and isinstance(posted_date, datetime):
            days_since_posted = (datetime.now() - posted_date).days
            if days_since_posted <= 3:
                return "1-3 days"
            elif days_since_posted <= 7:
                return "3-7 days"
            else:
                return "1-2 weeks"
        return "Unknown"
    
    async def _get_company_insights(self,
                                    session: AsyncSession,
                                    company_name: str) -> Optional[Dict[str, Any]]:
        try:
            query = text("""
                            SELECT
                                COUNT(*) AS total_postings,
                                COUNT(CASE WHEN posted_date >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as recent_postings,
                                AVG(salary_min) AS avg_min_salary,
                                AVG(salary_max) AS avg_max_salary
                            FROM job_postings
                            WHERE company_name = :company_name AND is_active = true
                        """)
            
            result = await session.execute(query, {'company_name': company_name})
            row = result.fetchone()
            
            if row and row.total_postings > 0:
                return {
                    'total_job_postings': row.total_postings,
                    'recent_activity': row.recent_postings,
                    'hiring_activity': 'High' if row.recent_postings > 5 else 'Moderate',
                    'avg_salary_range': {
                        'min': int(row.avg_min_salary) if row.avg_min_salary else None,
                        'max': int(row.avg_max_salary) if row.avg_max_salary else None
                    }
                }
            return None
        except Exception as e:
            logger.error(f"Error getting company insights for {company_name}: {str(e)}")
            return None
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        if cache_key not in self._cache:
            return False
        
        cached_time = self._cache[cache_key]['timestamp']
        return datetime.now() - cached_time < self._cache_ttle
    
    def _clear_user_cache(self, user_id: int):
        keys_to_remove = [key for key in self._cache.keys() if f"_{user_id}_" in key]
        for key in keys_to_remove:
            del self._cache[key]
    
    def _clear_all_user_caches(self):
        self._cache.clear()
    
job_matching_service = JobMatchingService()
