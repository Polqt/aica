"""
AI Components Module
Provides modular AI services for the AICA backend.
"""

from .skill_extraction import skill_extraction_service
from .job_matching import job_matching_ai_service
from .embeddings import embedding_service as ai_embedding_service
from .generation import generation_service

__all__ = [
    'skill_extraction_service',
    'job_matching_ai_service',
    'ai_embedding_service',
    'generation_service'
]