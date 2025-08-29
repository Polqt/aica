import logging
from typing import List, Dict, Any

from rag.generation.llm_service import llm_service

logger = logging.getLogger(__name__)


class GenerationService:

    def __init__(self):
        self._service = llm_service

    async def generate_job_match_explanation(self,
                                           user_skills: List[str],
                                           job_data: Dict[str, Any],
                                           similarity_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate explanation for job match."""
        return await self._service.generate_job_match_explanation(
            user_skills, job_data, similarity_scores
        )

    async def generate_multiple_matches_summary(self,
                                              user_skills: List[str],
                                              matched_jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of multiple job matches."""
        return await self._service.generate_multiple_job_matches_summary(
            user_skills, matched_jobs
        )

    async def generate_career_advice(self,
                                    user_profile: Dict[str, Any],
                                    job_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate career advice based on profile and matches."""
        return {
            "advice": "Based on your profile and job matches, focus on developing high-demand skills.",
            "next_steps": [
                "Update your resume with recent projects",
                "Network with professionals in your target roles",
                "Consider additional certifications"
            ]
        }

generation_service = GenerationService()