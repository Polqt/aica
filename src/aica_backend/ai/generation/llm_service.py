import logging
# import asyncpg

from typing import Dict, Any, List
from datetime import datetime

from ...core.config import settings
from .prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model_name = settings.OLLAMA_MODEL_NAME
        self.timeout = settings.OLLAMA_TIMEOUT
        self.prompt_templates = PromptTemplates()

    async def generate_job_match_explanation(self,
                                            user_skills: List[str],
                                            job_data: Dict[str, Any],
                                            similarity_scores: Dict[str, float]) -> Dict[str, Any]:
        """
            Generate explanation for why a job matches a user's skills.
        """
        
        try:
            prompt = self.prompt_templates.create_job_match_prompt(
                user_skills=user_skills,
                job_title=job_data['title'],
                company_name=job_data['company'],
                required_skills=job_data.get('required_skills', []),
                preferred_skills=job_data.get('preferred_skills', []),
                job_description=job_data.get('description', ''),
                similarity_score=similarity_scores.get('combined_similarity', 0.0)
            )
            
            response = await self._generate_completion(prompt)
            
            if not response:
                return self._create_fallback_explanation(user_skills, job_data, similarity_scores)
            
            explanation = self._parse_match_explanation(response, similarity_scores)
            
            return explanation
        except Exception as e:
            logger.error(f"Error generating job match explanation: {e}")
            return self._create_fallback_explanation(user_skills, job_data, similarity_scores)
        
    async def generate_skill_gap_analysis(self,
                                          user_skills: List[str],
                                          job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
            Generate analysis of skill gaps for a job position
        """
    
    async def generate_career_recommendations(self,
                                              user_skills: List[str],
                                              user_profile: Dict[str, Any],
                                              job_trends: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
            Generate a career development recommendations.
        """
                 
    def _create_fallback_explanation(self, user_skills: List[str],
                                    job_data: Dict[str, Any],
                                    similarity_scores: Dict[str, float]) -> Dict[str, Any]:
        
        score = similarity_scores.get('combined_similarity', 0.0)
        
        return {
            "overall_match_score": score,
            "match_strength": self._categorize_match_strength(score),
            "explanation": f"This {job_data['title']} position at {job_data['company_name']} shows a {score:.1%} compatibility with your skills profile based on our analysis.",
            "key_matching_skills": list(set(user_skills) & set(job_data.get('required_skills', []))),
            "skill_gaps": list(set(job_data.get('required_skills', [])) - set(user_skills)),
            "recommendations": "Consider developing the missing skills to strengthen your candidacy for this role.",
            "confidence": 0.7,
            "generated_at": datetime.utcnow().isoformat(),
            "fallback": True
        }
        
llm_service = LLMService()