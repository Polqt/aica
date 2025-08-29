import logging
import httpx
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...core.config import settings
from ...ai.generation.prompt_templates import PromptTemplates

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
        try:
            prompt = self.prompt_templates.create_job_match_prompt(
                user_skills=user_skills,
                job_title=job_data['title'],
                company_name=job_data.get('company_name', ''),
                required_skills=job_data.get('required_skills', []),
                preferred_skills=job_data.get('preferred_skills', []),
                job_description=job_data.get('description', ''),
                similarity_score=similarity_scores.get('combined_similarity', 0.0)
            )
            response = await self._generate_completion(prompt)
            if not response:
                return self._create_fallback_explanation(user_skills, job_data, similarity_scores)
            return self._parse_match_explanation(response, similarity_scores)
        except Exception as e:
            logger.error(f"Error generating job match explanation: {e}")
            return self._create_fallback_explanation(user_skills, job_data, similarity_scores)

    async def generate_multiple_job_matches_summary(self,
                                                    user_skills: List[str],
                                                    matched_jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            prompt = self.prompt_templates.create_multiple_matches_prompt(
                user_skills=user_skills,
                matched_jobs=matched_jobs[:5]
            )
            response = await self._generate_completion(prompt)
            if not response:
                return self._create_fallback_summary(user_skills, matched_jobs)
            return self._parse_matches_summary(response)
        except Exception as e:
            logger.error(f"Error generating multiple job matches summary: {e}")
            return self._create_fallback_summary(user_skills, matched_jobs)

    async def _generate_completion(self,
                                   prompt: str,
                                   max_tokens: int = 1000) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0,
                        "top_p": 1,
                        "top_k": 40,
                        "repeat_penalty": 1.1
                    }
                }
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    logger.error(f"Failed to generate completion: {response.status_code} - {response.text}")
                    return None
        except asyncio.TimeoutError:
            logger.error("Ollama API timeout")
            return None
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            return None

    def _parse_match_explanation(self,
                                response: str,
                                similarity_scores: Dict[str, float]) -> Dict[str, Any]:
        try:
            explanation = {
                "overall_match_score": similarity_scores.get('combined_similarity', 0.0),
                "match_strength": self._categorize_match_strength(
                    similarity_scores.get('combined_similarity', 0.0)
                ),
                "explanation": response,
                "key_matching_skills": [],
                "skill_gaps": [],
                "recommendations": "",
                "confidence": self._calculate_confidence(similarity_scores),
                "generated_at": datetime.now().isoformat()
            }
            return explanation
        except Exception as e:
            logger.error(f"Error parsing match explanation: {str(e)}")
            return {}

    def _parse_matches_summary(self, response: str) -> Dict[str, Any]:
        return {
            "recommendations": response,
            "skill_priorities": [],
            "career_paths": [],
            "next_steps": [],
            "timeline": "3-6 months",
            "generated_at": datetime.now().isoformat()
        }

    def _categorize_match_strength(self, score: float) -> str:
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

    def _calculate_confidence(self, similarity_scores: Dict[str, float]) -> float:
        combined_score = similarity_scores.get('combined_similarity', 0.0)
        skills_score = similarity_scores.get("skills_similarity", 0.0)
        score_variance = abs(combined_score - skills_score)
        confidence = combined_score * (1 - score_variance * 0.5)
        return max(0.1, min(1.0, confidence))

    def _create_fallback_explanation(self, user_skills: List[str],
                                    job_data: Dict[str, Any],
                                    similarity_scores: Dict[str, float]) -> Dict[str, Any]:
        score = similarity_scores.get('combined_similarity', 0.0)
        return {
            "overall_match_score": score,
            "match_strength": self._categorize_match_strength(score),
            "explanation": f"This {job_data['title']} position at {job_data.get('company_name','')} shows a {score:.1%} compatibility with your skills.",
            "key_matching_skills": list(set(user_skills) & set(job_data.get('required_skills', []))),
            "skill_gaps": list(set(job_data.get('required_skills', [])) - set(user_skills)),
            "recommendations": "Consider developing the missing skills to strengthen your candidacy for this role.",
            "confidence": 0.7,
            "generated_at": datetime.now().isoformat(),
            "fallback": True
        }

    def _create_fallback_summary(self,
                                 user_skills: List[str],
                                 matched_jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "summary": f"Found {len(matched_jobs)} job matches based on your {len(user_skills)} skills.",
            "top_industries": [],
            "common_skills": user_skills[:5],
            "trending_technologies": [],
            "career_insights": "Continue building on your existing skills while exploring related opportunities.",
            "generated_at": datetime.now().isoformat(),
            "fallback": True
        }

llm_service = LLMService()


