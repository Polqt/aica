"""
Job Management Service - Handles job search and management operations.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database.repositories.jobs import JobRepository
from ..rag.embeddings.embedding_service import embedding_service
from ..rag.embeddings.vector_store import vector_store
from ..core.config import settings
from ..utils.common import handle_service_error, create_success_response

logger = logging.getLogger(__name__)


class JobManagementService:
    """Service for managing job-related operations including search by skills."""

    def __init__(self):
        self.job_repository = JobRepository()

    async def search_jobs_by_skills(
        self,
        db: Session,
        skills: List[str],
        limit: int = 50,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for jobs based on user skills using vector similarity.

        Args:
            db: Database session
            skills: List of user skills
            limit: Maximum number of results to return
            threshold: Similarity threshold for matching

        Returns:
            List of matching jobs with similarity scores
        """
        try:
            if not skills:
                return []

            # Create skill embedding
            skills_text = " ".join(skills)
            skill_embedding = await embedding_service.encode_text(skills_text)

            # Search for similar jobs using vector store
            similar_jobs = await vector_store.find_similar_jobs(
                db, skill_embedding, limit=limit
            )

            # Filter by threshold and format results
            filtered_jobs = []
            for job in similar_jobs:
                similarity_score = job.get('similarity_score', 0.0)
                if similarity_score >= threshold:
                    filtered_jobs.append({
                        'job_id': job.get('id'),
                        'title': job.get('title'),
                        'company': job.get('company_name'),
                        'location': job.get('location'),
                        'similarity_score': similarity_score,
                        'matched_skills': self._find_matched_skills(skills, job),
                        'description': job.get('description', '')[:200] + '...' if job.get('description') else ''
                    })

            logger.info(f"Found {len(filtered_jobs)} jobs matching skills: {skills}")
            return filtered_jobs

        except Exception as e:
            logger.error(f"Error searching jobs by skills: {e}")
            return []

    def _find_matched_skills(self, user_skills: List[str], job: Dict[str, Any]) -> List[str]:
        """Find which user skills match the job requirements."""
        job_description = job.get('description', '').lower()
        job_title = job.get('title', '').lower()

        matched_skills = []
        for skill in user_skills:
            skill_lower = skill.lower()
            if (skill_lower in job_description or
                skill_lower in job_title):
                matched_skills.append(skill)

        return matched_skills

    async def get_job_recommendations(
        self,
        db: Session,
        user_id: int,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get personalized job recommendations for a user.

        Args:
            db: Database session
            user_id: User ID
            limit: Maximum number of recommendations

        Returns:
            List of recommended jobs
        """
        try:
            # Get user's profile and skills
            user_profile = self.job_repository.get_user_profile(db, user_id)
            if not user_profile:
                return []

            user_skills = [skill.name for skill in user_profile.skills] if user_profile.skills else []

            if not user_skills:
                # Return general recommendations if no skills
                return await self._get_general_recommendations(db, limit)

            # Search by skills
            recommendations = await self.search_jobs_by_skills(
                db, user_skills, limit=limit, threshold=0.5
            )

            logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
            return recommendations

        except Exception as e:
            logger.error(f"Error getting job recommendations for user {user_id}: {e}")
            return []

    async def _get_general_recommendations(
        self,
        db: Session,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get general job recommendations when user has no skills."""
        try:
            # Get recent jobs as general recommendations
            recent_jobs = self.job_repository.get_recent_jobs(db, limit=limit)

            recommendations = []
            for job in recent_jobs:
                recommendations.append({
                    'job_id': job.id,
                    'title': job.title,
                    'company': job.company_name,
                    'location': job.location,
                    'similarity_score': 0.0,  # No skill matching
                    'matched_skills': [],
                    'description': job.description[:200] + '...' if job.description else ''
                })

            return recommendations

        except Exception as e:
            logger.error(f"Error getting general recommendations: {e}")
            return []


# Create service instance
job_management_service = JobManagementService()