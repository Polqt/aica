import logging
from typing import List, Dict, Any

from core.config import settings
from rag.embeddings.embedding_service import embedding_service
from rag.embeddings.vector_store import vector_store

logger = logging.getLogger(__name__)


class JobMatchingAIService:

    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.similarity_threshold = settings.VECTOR_SIMILARITY_THRESHOLD

    async def calculate_match_score(self,
                                   user_skills: List[str],
                                   job_skills: List[str],
                                   job_description: str = "") -> Dict[str, Any]:
        """
        Calculate comprehensive match score between user and job.

        Args:
            user_skills: User's skills
            job_skills: Job's required skills
            job_description: Job description for additional context

        Returns:
            Dictionary with various similarity scores
        """
        try:
            user_embedding = self.embedding_service.encode_skills(user_skills)
            job_embedding = self.embedding_service.encode_skills(job_skills)
            skills_similarity = self.embedding_service.calculate_similarity(
                user_embedding, job_embedding
            )

            # Description-based similarity (if available)
            desc_similarity = 0.0
            if job_description:
                desc_embedding = self.embedding_service.encode_text(job_description)
                desc_similarity = self.embedding_service.calculate_similarity(
                    user_embedding, desc_embedding
                )

            # Calculate skill coverage
            skill_coverage = self._calculate_skill_coverage(user_skills, job_skills)

            # Weighted combined score
            combined_score = (
                0.6 * skills_similarity +
                0.3 * desc_similarity +
                0.1 * skill_coverage
            )

            return {
                "skills_similarity": float(skills_similarity),
                "description_similarity": float(desc_similarity),
                "skill_coverage": float(skill_coverage),
                "combined_score": float(combined_score),
                "match_strength": self._categorize_match_strength(combined_score)
            }

        except Exception as e:
            logger.error(f"Error calculating match score: {e}")
            return {
                "skills_similarity": 0.0,
                "description_similarity": 0.0,
                "skill_coverage": 0.0,
                "combined_score": 0.0,
                "match_strength": "Unknown",
                "error": str(e)
            }

    def _calculate_skill_coverage(self, user_skills: List[str], job_skills: List[str]) -> float:
        """Calculate what percentage of job skills the user has."""
        if not job_skills:
            return 1.0  # If no skills required, perfect coverage

        user_skills_lower = [skill.lower() for skill in user_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]

        matching_skills = 0
        for job_skill in job_skills_lower:
            # Check for exact match or partial match
            if any(job_skill in user_skill or user_skill in job_skill
                   for user_skill in user_skills_lower):
                matching_skills += 1

        return matching_skills / len(job_skills)

    def _categorize_match_strength(self, score: float) -> str:
        """Categorize match strength based on score."""
        if score >= 0.8:
            return "Excellent Match"
        elif score >= 0.7:
            return "Very Good Match"
        elif score >= 0.6:
            return "Good Match"
        elif score >= 0.5:
            return "Fair Match"
        else:
            return "Weak Match"

    async def generate_match_insights(self,
                                     user_skills: List[str],
                                     job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate detailed insights about a job match.
        """
        try:
            job_skills = job_data.get('required_skills', []) + job_data.get('preferred_skills', [])
            match_scores = await self.calculate_match_score(
                user_skills, job_skills, job_data.get('description', '')
            )

            # Identify skill gaps
            skill_gaps = self._identify_skill_gaps(user_skills, job_skills)

            # Generate recommendations
            recommendations = self._generate_recommendations(match_scores, skill_gaps)

            return {
                "match_scores": match_scores,
                "skill_gaps": skill_gaps,
                "recommendations": recommendations,
                "key_matching_skills": [skill for skill in job_skills
                                      if any(user_skill.lower() in skill.lower()
                                            for user_skill in user_skills)]
            }

        except Exception as e:
            logger.error(f"Error generating match insights: {e}")
            return {
                "match_scores": {},
                "skill_gaps": [],
                "recommendations": ["Unable to generate insights"],
                "error": str(e)
            }

    def _identify_skill_gaps(self, user_skills: List[str], job_skills: List[str]) -> List[str]:
        """Identify skills the user lacks for the job."""
        user_skills_lower = [skill.lower() for skill in user_skills]
        skill_gaps = []

        for job_skill in job_skills:
            job_skill_lower = job_skill.lower()
            if not any(job_skill_lower in user_skill or user_skill in job_skill_lower
                      for user_skill in user_skills_lower):
                skill_gaps.append(job_skill)

        return skill_gaps

    def _generate_recommendations(self, match_scores: Dict[str, Any], skill_gaps: List[str]) -> List[str]:
        """Generate actionable recommendations based on match analysis."""
        recommendations = []
        combined_score = match_scores.get('combined_score', 0.0)

        if combined_score >= 0.8:
            recommendations.append("Strong match! Prepare your application with confidence.")
        elif combined_score >= 0.6:
            recommendations.append("Good match with room for improvement.")
        else:
            recommendations.append("Consider developing additional skills for better fit.")

        # Skill gap recommendations
        if skill_gaps:
            if len(skill_gaps) <= 3:
                recommendations.append(f"Consider learning: {', '.join(skill_gaps)}")
            else:
                recommendations.append(f"Consider learning: {', '.join(skill_gaps[:3])} and {len(skill_gaps) - 3} more skills")

        return recommendations

job_matching_ai_service = JobMatchingAIService()