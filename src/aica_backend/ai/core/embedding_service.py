import logging
import numpy as np

from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from functools import lru_cache

from ...core.config import settings
from ..interfaces import EmbeddingServiceInterface

logger = logging.getLogger(__name__)

class EmbeddingService(EmbeddingServiceInterface):
    
    def __init__(self):
        super.model = self._load_model()
        self.dimension = settings.EMBEDDING_DIMENSION
    
    
    def _load_model(self) -> SentenceTransformer:
        try:
            model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            return model
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    @lru_cache(maxsize=1000)
    def encode_skills(self, skills: tuple) -> np.ndarray:
        if not skills:
            return np.zeros(self.dimension)
        
        skills_text = " ".join(skills)
        return self.model.encode(skills_text, normalize_embeddings=True)
    
    def encode_skills(self, skills: List[str]) -> np.ndarray:
        return self._encode_skills_cached(tuple(skills))
    
    def encode_text(self, text: str) -> np.ndarray:
        if not text.strip():
            return np.zeros(self.dimension)
        
        return self.model.encode(text, normalize_embeddings=True)
    
    def encode_job_content(
        self, 
        title: str, 
        description: str, 
        required_skills: List[str],
        preferred_skills: List[str] = None
    ) -> Dict[str, np.ndarray]:
        preferred_skills = preferred_skills or []
        
        # Combine all skills
        all_skills = required_skills + preferred_skills
        skills_embedding = self.encode_skills(all_skills)
        
        # Create job description embedding
        full_text = f"{title}. {description}"
        description_embedding = self.encode_text(full_text)
        
        return {
            "skills": skills_embedding,
            "description": description_embedding,
            "combined": (skills_embedding + description_embedding) / 2
        }
    
    def calculate_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calculate cosine similarity between embeddings."""
        if emb1.size == 0 or emb2.size == 0:
            return 0.0
        
        dot_product = np.dot(emb1, emb2)
        norm_product = np.linalg.norm(emb1) * np.linalg.norm(emb2)
        
        if norm_product == 0:
            return 0.0
        
        return float(dot_product / norm_product)
    