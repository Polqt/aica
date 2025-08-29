import logging
from typing import List, Dict, Any
import numpy as np

from rag.embeddings.embedding_service import embedding_service

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self._service = embedding_service

    async def encode_text(self, text: str) -> np.ndarray:
        """Encode text into embeddings."""
        return self._service.encode_text(text)

    async def encode_skills(self, skills: List[str]) -> np.ndarray:
        """Encode skills into embeddings."""
        return self._service.encode_skills(skills)

    async def encode_job(self, title: str, description: str,
                        required_skills: List[str] = None,
                        preferred_skills: List[str] = None) -> Dict[str, np.ndarray]:
        """Encode job information into embeddings."""
        return self._service.encode_job_description(
            title, description, required_skills, preferred_skills
        )

    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate similarity between two embeddings."""
        return self._service.calculate_similarity(embedding1, embedding2)

    def get_stats(self) -> Dict[str, Any]:
        """Get embedding service statistics."""
        return self._service.get_embedding_stats()

embedding_service = EmbeddingService()