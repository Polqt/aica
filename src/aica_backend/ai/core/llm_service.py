import logging

from typing import List, Dict, Any
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ...core.config import settings
from ..interfaces import LLMServiceInterface

logger = logging.getLogger(__name__)

class OllamaLLMService(LLMServiceInterface):
    
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL_NAME,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0
        )
        
    async def generate_job_explanation(self, user_skills: List[str], job_data: Dict[str, Any]) -> str:
        prompt = ChatPromptTemplate.from_template("""
        You are a career counselor. Explain why this job is a good match for the candidate.
        Be specific about skill alignment and provide actionable insights.
        
        Candidate Skills: {user_skills}
        
        Job Details:
        - Title: {job_title}
        - Company: {company}
        - Required Skills: {required_skills}
        - Experience Level: {experience_level}
        
        Provide a concise, encouraging explanation (max 150 words):
        """)
        
        chain = prompt | self.llm | self.output_parser
        
        try:
            response = await chain.ainvoke({
                "user_skills": ", ".join(user_skills),
                "job_title": job_data.get('title', 'N/A'),
                "company": job_data.get('company', 'N/A'),
                "required_skills": ", ".join(job_data.get('skills', [])),
                "experience_level": job_data.get('experience_level', 'N/A')
            })
            return response.strip()
        except Exception as e:
            logger.error(f"Failed to generate job explanation: {e}")
            return "This role appears to be a strong match based on your skills and experience."
    
    async def generate_career_insights(
        self, 
        user_profile: Dict[str, Any], 
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        prompt = ChatPromptTemplate.from_template("""
        Analyze this professional's career situation and provide strategic insights.
        
        Profile:
        - Skills: {skills}
        - Experience: {experience_years} years
        - Current Role: {current_role}
        
        Market Data:
        - High-demand skills in their area: {trending_skills}
        - Average salary range: {salary_range}
        
        Provide insights in this format:
        STRENGTHS: (2-3 key strengths)
        OPPORTUNITIES: (2-3 growth areas)
        RECOMMENDATIONS: (2-3 actionable next steps)
        """)
        
        chain = prompt | self.llm | self.output_parser
        
        try:
            response = await chain.ainvoke({
                "skills": ", ".join(user_profile.get('skills', [])),
                "experience_years": user_profile.get('experience_years', 0),
                "current_role": user_profile.get('title', 'Professional'),
                "trending_skills": ", ".join(market_data.get('trending_skills', [])),
                "salary_range": market_data.get('salary_range', 'Not available')
            })

            sections = {}
            current_section = None
            
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith(('STRENGTHS:', 'OPPORTUNITIES:', 'RECOMMENDATIONS:')):
                    current_section = line.replace(':', '').lower()
                    sections[current_section] = []
                elif line and current_section:
                    sections[current_section].append(line)
            
            return {
                'strengths': sections.get('strengths', []),
                'opportunities': sections.get('opportunities', []),
                'recommendations': sections.get('recommendations', []),
                'raw_response': response
            }
            
        except Exception as e:
            logger.error(f"Failed to generate career insights: {e}")
            return {
                'strengths': ['Strong technical foundation'],
                'opportunities': ['Explore emerging technologies'],
                'recommendations': ['Continue skill development'],
                'error': str(e)
            }
            