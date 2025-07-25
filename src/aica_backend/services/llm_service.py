# Purpose: Handle OLLAMA integration for job data extraction
# Components:
# - OllamaClient wrapper
# - Job extraction prompts
# - Structured output parsing
# - Error handling for LLM failures

from ..api.v1.schemas.jobs import JobDetails
from ..core.config import settings


class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model_name = settings.OLLAMA_MODEL_NAME
        self.timeout = settings.OLLAMA_TIMEOUT

    async def extract_job_details(self, raw_text: str) -> JobDetails:
        # OLLAMA API integration
        # Structured output parsing
        # Error handling with retries
        pass
    
    async def health_check(self) -> bool:
        # Check if OLLAMA is running
        pass
    
    def get_extraction_prompt(self) -> str:
        # Optimized prompt for job data extraction
        pass