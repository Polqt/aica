import numpy as np

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

class EmbeddingServiceInterface(ABC):
    
    @abstractmethod
    def encode_skills(self, skills: List[str]) -> np.ndarray:
        """Generate embedding for a list of skills."""
        pass
    
    @abstractmethod
    def encode_text(self, text: str) -> np.ndarray:
        """Generate embedding for text content."""
        pass

    @abstractmethod
    def calculate_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calculate similarity between two embeddings."""
        pass

class VectorStoreInterface(ABC):
    
    @abstractmethod
    async def store_job_embedding(
        self,
        session: AsyncSession,
        job_id: int,
        embeddings: Dict[str, np.ndarray]
    ) -> bool:
        """Store job embeddings in the vector store."""
        pass
    
    @abstractmethod
    async def find_similar_jobs(
        self,
        session: AsyncSession,
        query_embedding: np.ndarray,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Find jobs similar to the query embedding."""
        pass
    
class LLMServiceInterface(ABC):
    
    @abstractmethod
    async def generate_job_explanation(
        self, 
        user_skills: List[str],
        job_data: Dict[str, Any],
    ) -> str:
        """Generate explanation for job match."""
        pass
    
    @abstractmethod
    async def generate_career_insights(
        self,
        user_profile: Dict[str, Any],
        market_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate career insights based on user profile and market data."""
        pass
    