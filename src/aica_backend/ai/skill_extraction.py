import logging
from typing import List, Dict, Any

from utils.common import clean_text
from rag.generation.llm_service import llm_service

logger = logging.getLogger(__name__)


class SkillExtractionService:
    """
    Service for extracting and processing skills from various sources.
    """

    def __init__(self):
        self.technical_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask'],
            'data': ['sql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'ml': ['machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy']
        }

        self.soft_skills = [
            'communication', 'leadership', 'problem solving', 'teamwork',
            'project management', 'agile', 'scrum', 'analytical thinking'
        ]

    async def extract_skills_from_job(self, job_description: str, job_title: str = "") -> Dict[str, Any]:
        """
        Extract skills from job description using multiple methods.
        """
        try:
            # Method 1: Pattern-based extraction
            pattern_skills = self._extract_skills_pattern(job_description)

            # Method 2: LLM-based extraction (if available)
            llm_skills = await self._extract_skills_llm(job_description, job_title)

            # Combine and deduplicate
            combined_skills = self._combine_skill_results(pattern_skills, llm_skills)

            return {
                "technical_skills": combined_skills.get("technical", []),
                "soft_skills": combined_skills.get("soft", []),
                "extraction_method": "hybrid",
                "confidence": combined_skills.get("confidence", 0.8)
            }

        except Exception as e:
            logger.error(f"Error extracting skills from job: {e}")
            return {
                "technical_skills": [],
                "soft_skills": [],
                "extraction_method": "failed",
                "error": str(e)
            }

    def _extract_skills_pattern(self, text: str) -> Dict[str, Any]:
        """Extract skills using pattern matching."""
        text_lower = clean_text(text).lower()
        technical_skills = []
        soft_skills = []

        # Extract technical skills
        for category, keywords in self.technical_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    technical_skills.append(keyword.title())

        # Extract soft skills
        for skill in self.soft_skills:
            if skill.replace(' ', '') in text_lower or skill in text_lower:
                soft_skills.append(skill.title())

        return {
            "technical": list(set(technical_skills)),
            "soft": list(set(soft_skills)),
            "confidence": 0.7
        }

    async def _extract_skills_llm(self, job_description: str, job_title: str = "") -> Dict[str, Any]:
        """Extract skills using LLM for more accurate results."""
        try:
            if not llm_service:
                return {"technical": [], "soft": [], "confidence": 0.0}

            prompt = f"""
            Extract technical and soft skills from the following job posting:

            Job Title: {job_title}
            Description: {job_description}

            Return a JSON object with:
            - technical_skills: array of technical skills mentioned
            - soft_skills: array of soft skills mentioned

            Focus on skills that are explicitly mentioned or clearly implied.
            """

            # This would use the LLM service to extract skills
            # For now, return empty as we don't want to make actual LLM calls
            return {"technical": [], "soft": [], "confidence": 0.0}

        except Exception as e:
            logger.error(f"Error in LLM skill extraction: {e}")
            return {"technical": [], "soft": [], "confidence": 0.0}

    def _combine_skill_results(self, pattern_result: Dict, llm_result: Dict) -> Dict[str, Any]:
        """Combine results from different extraction methods."""
        combined_technical = list(set(
            pattern_result.get("technical", []) + llm_result.get("technical", [])
        ))

        combined_soft = list(set(
            pattern_result.get("soft", []) + llm_result.get("soft", [])
        ))

        # Use pattern matching confidence as base, boost if LLM agrees
        confidence = pattern_result.get("confidence", 0.7)
        if llm_result.get("technical") or llm_result.get("soft"):
            confidence = min(confidence + 0.2, 0.95)

        return {
            "technical": combined_technical,
            "soft": combined_soft,
            "confidence": confidence
        }

    def validate_skill_list(self, skills: List[str]) -> List[str]:
        """Validate and clean a list of skills."""
        validated = []
        for skill in skills:
            if isinstance(skill, str) and skill.strip():
                cleaned = clean_text(skill)
                if len(cleaned) >= 2 and len(cleaned) <= 50:  # Reasonable length limits
                    validated.append(cleaned)

        return list(set(validated))  # Remove duplicates

skill_extraction_service = SkillExtractionService()