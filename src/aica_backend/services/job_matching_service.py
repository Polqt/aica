"""
Job Matching Service - Core business logic for matching users with jobs.
Integrates RAG pipeline, embeddings, and similarity search.
Follows clean code principles with clear separation of concerns.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..rag.pipeline.rag_pipeline import rag_pipeline
from ..rag.embeddings.embedding_service import embedding_service
from ..database.repositories.jobs import JobRepository
from ..database.repositories.profile import ProfileRepository
from ..core.config import settings
from ..utils.common import handle_service_error, create_success_response, ValidationError, NotFoundError

logger = logging.getLogger(__name__)


class JobMatchingService:
    """
    Comprehensive job matching service using RAG and vector similarity.
    Follows single responsibility principle with focused methods.
    """

    def __init__(self):
        self.rag_pipeline = rag_pipeline
        self.embedding_service = embedding_service
        self.job_repo = JobRepository()
        self.profile_repo = ProfileRepository()

    async def find_job_matches(
        self,
        user_id: int,
        db: AsyncSession,
        limit: int = 20,
        min_similarity: float = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Find job matches for a user using RAG pipeline.
        Clean, focused method with clear parameters and return structure.
        """
        try:
            # Get user profile and skills
            user_profile = await self._get_user_profile(user_id, db)
            if not user_profile:
                raise NotFoundError("User profile not found")

            user_skills = user_profile.get('skills', [])
            if not user_skills:
                raise ValidationError("No skills found in user profile")

            # Use RAG pipeline for intelligent matching
            matches_result = await self.rag_pipeline.find_matching_jobs(
                session=db,
                user_id=user_id,
                user_skills=user_skills,
                filters=filters,
                limit=limit,
                generate_explanation=True
            )

            # Apply minimum similarity filter if specified
            if min_similarity:
                matches_result = self._filter_by_similarity(
                    matches_result, min_similarity
                )

            # Add metadata for better API responses
            matches_result.update({
                "user_id": user_id,
                "total_skills_analyzed": len(user_skills),
                "filters_applied": filters or {},
                "min_similarity_threshold": min_similarity or settings.VECTOR_SIMILARITY_THRESHOLD
            })

            logger.info(f"Found {matches_result.get('total_matches', 0)} matches for user {user_id}")
            return matches_result

        except Exception as e:
            logger.error(f"Error finding job matches for user {user_id}: {e}")
            return handle_service_error(e, f"Job matching failed for user {user_id}")

    async def get_similar_jobs(
        self,
        job_id: int,
        db: AsyncSession,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Find jobs similar to a given job.
        Clean implementation using vector similarity.
        """
        try:
            # Get the target job
            target_job = await self.job_repo.get_by_id(db, job_id)
            if not target_job:
                return self._create_empty_response("Target job not found")

            # Extract skills for similarity search
            job_skills = target_job.technical_skills or []
            if target_job.soft_skills:
                job_skills.extend(target_job.soft_skills)

            if not job_skills:
                return self._create_empty_response("No skills found for target job")

            # Find similar jobs using skill-based similarity
            similar_jobs = await self._find_similar_jobs_by_skills(
                job_skills, db, limit, exclude_job_id=job_id
            )

            return {
                "target_job": {
                    "id": target_job.id,
                    "title": target_job.job_title,
                    "company": target_job.company_name,
                    "skills": job_skills
                },
                "similar_jobs": similar_jobs,
                "total_similar": len(similar_jobs)
            }

        except Exception as e:
            logger.error(f"Error finding similar jobs for job {job_id}: {e}")
            return self._create_error_response(str(e))

    async def analyze_job_match(
        self,
        user_id: int,
        job_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Provide detailed analysis of job-user match.
        Comprehensive analysis using multiple AI techniques.
        """
        try:
            # Get user profile and job details
            user_profile = await self._get_user_profile(user_id, db)
            job_details = await self.job_repo.get_by_id(db, job_id)

            if not user_profile:
                return self._create_error_response("User profile not found")
            if not job_details:
                return self._create_error_response("Job not found")

            user_skills = user_profile.get('skills', [])
            job_skills = (job_details.technical_skills or []) + (job_details.soft_skills or [])

            # Calculate similarity scores
            similarity_scores = await self._calculate_detailed_similarity(
                user_skills, job_skills, job_details
            )

            # Generate AI-powered analysis
            analysis = await self._generate_match_analysis(
                user_profile, job_details, similarity_scores
            )

            return {
                "user_id": user_id,
                "job_id": job_id,
                "similarity_scores": similarity_scores,
                "analysis": analysis,
                "recommendations": self._generate_recommendations(
                    similarity_scores, user_skills, job_skills
                )
            }

        except Exception as e:
            logger.error(f"Error analyzing job match for user {user_id}, job {job_id}: {e}")
            return self._create_error_response(str(e))

    async def _get_user_profile(self, user_id: int, db: AsyncSession) -> Optional[Dict[str, Any]]:
        """Clean helper method to get user profile data."""
        try:
            profile = await self.profile_repo.get_by_user_id(db, user_id)
            if not profile:
                return None

            return {
                "id": profile.id,
                "user_id": profile.user_id,
                "skills": profile.skills or [],
                "experience_level": profile.experience_level,
                "preferred_job_types": profile.preferred_job_types or []
            }
        except Exception as e:
            logger.error(f"Error getting user profile for user {user_id}: {e}")
            return None

    async def _find_similar_jobs_by_skills(
        self,
        skills: List[str],
        db: AsyncSession,
        limit: int,
        exclude_job_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Find jobs similar to given skills using vector search."""
        try:
            # Create embedding for skills
            skills_embedding = self.embedding_service.encode_skills(skills)

            # Use vector store for similarity search
            from ..rag.embeddings.vector_store import vector_store
            similar_jobs = await vector_store.find_similar_jobs(
                db, skills_embedding, limit=limit
            )

            # Filter out excluded job if specified
            if exclude_job_id:
                similar_jobs = [
                    job for job in similar_jobs
                    if job.get('id') != exclude_job_id
                ]

            return similar_jobs

        except Exception as e:
            logger.error(f"Error finding similar jobs by skills: {e}")
            return []

    async def _calculate_detailed_similarity(
        self,
        user_skills: List[str],
        job_skills: List[str],
        job_details
    ) -> Dict[str, float]:
        """Calculate detailed similarity scores between user and job."""
        try:
            # Skill-based similarity
            user_embedding = self.embedding_service.encode_skills(user_skills)
            job_embedding = self.embedding_service.encode_skills(job_skills)
            skill_similarity = self.embedding_service.calculate_similarity(
                user_embedding, job_embedding
            )

            # Description-based similarity (if available)
            desc_similarity = 0.0
            if job_details.full_text:
                desc_embedding = self.embedding_service.encode_text(job_details.full_text)
                desc_similarity = self.embedding_service.calculate_similarity(
                    user_embedding, desc_embedding
                )

            # Combined similarity score
            combined_similarity = 0.7 * skill_similarity + 0.3 * desc_similarity

            return {
                "skill_similarity": float(skill_similarity),
                "description_similarity": float(desc_similarity),
                "combined_similarity": float(combined_similarity)
            }

        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return {"skill_similarity": 0.0, "description_similarity": 0.0, "combined_similarity": 0.0}

    async def _generate_match_analysis(
        self,
        user_profile: Dict[str, Any],
        job_details,
        similarity_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate AI-powered match analysis."""
        try:
            # Use LLM service for analysis
            from ..rag.generation.llm_service import llm_service

            analysis = await llm_service.generate_job_match_explanation(
                user_skills=user_profile.get('skills', []),
                job_data={
                    'title': job_details.job_title,
                    'company_name': job_details.company_name,
                    'required_skills': job_details.technical_skills or [],
                    'preferred_skills': job_details.soft_skills or [],
                    'description': job_details.full_text or ''
                },
                similarity_scores=similarity_scores
            )

            return analysis

        except Exception as e:
            logger.error(f"Error generating match analysis: {e}")
            return {"error": "Unable to generate analysis", "fallback": True}

    def _generate_recommendations(
        self,
        similarity_scores: Dict[str, float],
        user_skills: List[str],
        job_skills: List[str]
    ) -> List[str]:
        """Generate actionable recommendations based on match analysis."""
        recommendations = []
        combined_score = similarity_scores.get('combined_similarity', 0.0)

        if combined_score >= 0.8:
            recommendations.append("Strong match! Prepare your application with confidence.")
        elif combined_score >= 0.6:
            recommendations.append("Good match with room for improvement.")
        else:
            recommendations.append("Consider developing additional skills for better fit.")

        # Skill gap recommendations
        missing_skills = set(job_skills) - set(user_skills)
        if missing_skills:
            recommendations.append(f"Consider learning: {', '.join(list(missing_skills)[:3])}")

        return recommendations

    def _filter_by_similarity(self, matches_result: Dict[str, Any], min_similarity: float) -> Dict[str, Any]:
        """Filter matches by minimum similarity threshold."""
        filtered_matches = []
        for match in matches_result.get('matches', []):
            similarity = match.get('similarity_scores', {}).get('combined_similarity', 0.0)
            if similarity >= min_similarity:
                filtered_matches.append(match)

        matches_result['matches'] = filtered_matches
        matches_result['total_matches'] = len(filtered_matches)
        return matches_result

    def _create_empty_response(self, message: str) -> Dict[str, Any]:
        """Clean helper for empty responses."""
        return {
            "matches": [],
            "total_matches": 0,
            "message": message,
            "processing_time": 0
        }

    def _create_error_response(self, error: str) -> Dict[str, Any]:
        """Clean helper for error responses."""
        return {
            "matches": [],
            "total_matches": 0,
            "error": error,
            "processing_time": 0
        }


# Singleton instance for clean imports
job_matching_service = JobMatchingService()