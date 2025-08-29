from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

from ..embeddings.embedding_service import embedding_service
from ..embeddings.store_factory import get_vector_store
from ..generation.llm_service import llm_service
from ...core.config import settings

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_store = get_vector_store()
        self.llm_service = llm_service

        # Initialize LangChain components
        self._setup_langchain_components()

    def _setup_langchain_components(self):
        """Setup LangChain components for RAG pipeline."""
        try:
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL_NAME
            )

            # Initialize LLM
            self.llm = Ollama(
                model=settings.OLLAMA_MODEL_NAME,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0.1
            )

            # Setup prompt templates
            self._setup_prompts()

        except Exception as e:
            logger.error(f"Error setting up LangChain components: {e}")
            # Fallback to existing services
            self.embeddings = None
            self.llm = None

    def _setup_prompts(self):
        """Setup reusable prompt templates."""
        self.job_match_prompt = PromptTemplate(
            input_variables=["user_skills", "job_title", "company", "job_description", "similarity_score"],
            template="""
            Analyze the compatibility between a user's skills and a job posting.

            User Skills: {user_skills}
            Job Title: {job_title}
            Company: {company}
            Job Description: {job_description}
            Similarity Score: {similarity_score}

            Provide a detailed analysis including:
            1. Overall match strength (Excellent/Good/Fair/Weak)
            2. Key matching skills
            3. Missing skills gaps
            4. Specific recommendations

            Format your response as JSON with keys: match_strength, matching_skills, skill_gaps, recommendations
            """
        )

        self.skill_extraction_prompt = PromptTemplate(
            input_variables=["job_description"],
            template="""
            Extract technical and soft skills from the following job description.
            Focus on programming languages, frameworks, tools, and soft skills.

            Job Description: {job_description}

            Return a JSON object with:
            - technical_skills: array of technical skills
            - soft_skills: array of soft skills
            - categories: object with skill categories
            """
        )

    async def extract_job_skills_langchain(self, job_description: str) -> Dict[str, Any]:
        """
        Extract skills from job description using LangChain.

        Args:
            job_description: The job description text

        Returns:
            Dictionary with technical_skills, soft_skills, and categories
        """
        try:
            if not self.llm:
                # Fallback to existing service
                return await self._extract_skills_fallback(job_description)

            # Create the chain
            chain = self.skill_extraction_prompt | self.llm | JsonOutputParser()

            # Run the chain
            result = await chain.ainvoke({"job_description": job_description})

            return {
                "technical_skills": result.get("technical_skills", []),
                "soft_skills": result.get("soft_skills", []),
                "categories": result.get("categories", {})
            }

        except Exception as e:
            logger.error(f"Error extracting skills with LangChain: {e}")
            return await self._extract_skills_fallback(job_description)

    async def _extract_skills_fallback(self, job_description: str) -> Dict[str, Any]:
        """Fallback skill extraction method."""
        # Simple pattern-based extraction
        from ...utils.common import clean_text

        text = clean_text(job_description).lower()

        # Common technical skills
        tech_skills = []
        tech_patterns = [
            'python', 'java', 'javascript', 'react', 'node.js', 'django', 'flask',
            'sql', 'postgresql', 'mongodb', 'machine learning', 'ai', 'nlp',
            'docker', 'kubernetes', 'aws', 'git', 'linux', 'html', 'css'
        ]

        for skill in tech_patterns:
            if skill in text:
                tech_skills.append(skill.title())

        return {
            "technical_skills": tech_skills,
            "soft_skills": ["Communication", "Problem Solving"],  # Default soft skills
            "categories": {"technical": tech_skills, "soft": ["Communication", "Problem Solving"]}
        }

    async def find_matching_jobs(self,
                                session: AsyncSession,
                                user_id: int,
                                user_skills: List[str],
                                filters: Optional[Dict[str, Any]] = None,
                                limit: int = 20,
                                generate_explanation: bool = True) -> Dict[str, Any]:
        try:
            start_time = datetime.now()
            user_skills_embedding = self.embedding_service.encode_skills(user_skills)
            await self.vector_store.store_user_profile_embedding(session, user_id, user_skills_embedding)
            if filters:
                matched_jobs = await self.vector_store.get_job_recommendations_by_filters(
                    session, user_skills_embedding, filters, limit
                )
            else:
                matched_jobs = await self.vector_store.find_similar_jobs(
                    session, user_skills_embedding, limit
                )
            if not matched_jobs:
                return {"matches": [], "total_matches": 0, "user_skills": user_skills,
                        "processing_time": (datetime.now() - start_time).total_seconds(),
                        "explanation_generated": False}
            explanations = {}
            if generate_explanation:
                explanations = await self._generate_match_explanation(user_skills, matched_jobs[:5])
            enhanced_matches = self._enhance_matches_with_explanations(matched_jobs, explanations)
            summary = None
            if generate_explanation and matched_jobs:
                summary = await self.llm_service.generate_multiple_job_matches_summary(user_skills, matched_jobs)
            processing_time = (datetime.now() - start_time).total_seconds()
            return {
                "matches": enhanced_matches,
                "total_matches": len(matched_jobs),
                "user_skills": user_skills,
                "summary": summary,
                "processing_time": processing_time,
                "explanations_generated": generate_explanation,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in job matching pipeline: {str(e)}")
            return {"matches": [], "total_matches": 0, "user_skills": user_skills,
                    "error": str(e), "processing_time": 0, "explanations_generated": False}

    async def _generate_match_explanation(self,
                                          user_skills: List[str],
                                          matched_jobs: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        explanations = {}
        tasks = []
        for job_data in matched_jobs:
            task = self.llm_service.generate_job_match_explanation(
                user_skills,
                job_data,
                job_data.get('similarity_scores', {})
            )
            tasks.append((job_data['id'], task))
        for job_id, task in tasks:
            try:
                explanation = await task
                explanations[job_id] = explanation
            except Exception as e:
                logger.error(f"Failed to generate explanation for job {job_id}: {str(e)}")
                explanations[job_id] = {"error": str(e), "explanation": "Unable to generate explanation at this time", "fallback": True}
        return explanations

    def _enhance_matches_with_explanations(self,
                                           matched_jobs: List[Dict[str, Any]],
                                           explanations: Dict[int, Dict[str, Any]]) -> List[Dict[str, Any]]:
        enhanced_matches = []
        for job_data in matched_jobs:
            job_id = job_data.get('id')
            enhanced_job = job_data.copy()
            if job_id in explanations:
                enhanced_job['ai_explanation'] = explanations[job_id]
            enhanced_matches.append(enhanced_job)
        return enhanced_matches

rag_pipeline = RAGPipeline()

async def find_matching_jobs(session: AsyncSession, user_id: int, user_skills: List[str], **kwargs) -> Dict[str, Any]:
    return await rag_pipeline.find_matching_jobs(session, user_id, user_skills, **kwargs)


