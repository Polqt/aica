import logging
import numpy as np
import asyncio
import threading

from typing import List
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor

from ...core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL_NAME
        self.dimension = settings.EMBEDDING_DIMENSION
        self._model = None
        self._executor = ThreadPoolExecutor(max_workers=2)
        self._lock = threading.Lock()
    
    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    logger.info(f"Loading embedding model: {self.model_name}")
                    self._model = SentenceTransformer(self.model_name)
                    logger.info("Embedding model loaded successfully.")
        return self._model
    
    def encode_text(self, text: str) -> np.ndarray:
        
        if not text or not text.strip():
            return np.zeros(self.dimension)
        
        try:
            cleaned_text = self._preprocess_text(text)
            
            embedding = self.model.encode(
                cleaned_text,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            return embedding.astype(np.float32)
        
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return np.zeros(self.dimension)
    
    def encode_texts(self, texts: List[str]) -> List[np.ndarray]:
        if not texts:
            return []
        
        try:
            cleaned_texts = [self._preprocess_text(text) for text in texts]
            
            embeddings = self.model.encode(
                cleaned_texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
                batch_size=32,
            )
            
            return [emb.astype(np.float32) for emb in embeddings]
        except Exception as e:
            logger.error(f"Error encoding texts: {e}")
            return [np.zeros(self.dimension) for _ in texts]
        
    async def encode_text_async(self, text: str) -> np.ndarray:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self.encode_text, text)
    
    async def encode_texts_async(self, texts: List[str]) -> List[np.ndarray]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self.encode_texts, texts)
    
    def encode_skills(self, skills: List[str]) -> np.ndarray:
        if not skills:
            return np.zeros(self.dimension)
        
        skills_text = self._format_skills_for_embedding(skills)
        return self.encode_text(skills_text)
    
    def encode_job_description(self, title: str, description: str,
                               required_skills: List[str] = None,
                               preferred_skills: List[str] = None
                               ) -> dict:
        
        embeddings = {}
        
        embeddings['title'] = self.encode_text(title)
        embeddings['description'] = self.encode_text(description)
        
        all_skills = []
        if required_skills:
            all_skills.extend(required_skills)
        if preferred_skills:
            all_skills.extend(preferred_skills)
            
        if all_skills:
            embeddings['skills'] = self.encode_skills(all_skills)
        else:
            embeddings['skills'] = np.zeros(self.dimension)
            
        embeddings['combined'] = self._create_combined_embedding(
            embeddings['title'],
            embeddings['description'],
            embeddings['skills'],
            weights={
                'title': 0.3,
                'description': 0.4,
                'skills': 0.3,
            }
        )
        
        return embeddings
    def calculate_similarity(self, embedding1: np.ndarray,
                            embedding2: np.ndarray) -> float:
        """
            Calculate cosine similarity between two embeddings.
            Returns to cosine similarity score (0-1)
        """
        
        try:
            if np.allclose(embedding1, 0) or np.allclose(embedding2, 0):
                return 0.0
            
            similarity = np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
            )
            
            return max(0.0, min(1.0, similarity))
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_most_similar(self, query_embedding: np.ndarray,
                          candidate_embeddings: List[np.ndarray],
                          top_k: int = 10) -> List[tuple]:
        
        """
            Find ya na di ang mosst similar embeddings to query.
            Returns a list of tuples containing the index and similarity score of the most similar embeddings.
        """
        
        if not candidate_embeddings:
            return []
        
        similarities = []
        
        for i, candidate in enumerate(candidate_embeddings):
            similarity = self.calculate_similarity(query_embedding, candidate)
            similarities.append((i, similarity))
        return similarities[:top_k]
    
    def _preprocess_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = text.strip()
        
        # Remove whitespace
        text = ' '.join(text.split())    
        
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        return text
    
    def _format_skills_for_embedding(self, skills: List[str]) -> str:
        """
            Format skills list for optimal embedding generation.
        """
        
        cleaned_skills = list(set(skill.strip() for skill in skills if skill.strip()))
        
        if len(cleaned_skills) == 1:
            return f"Skill: {cleaned_skills[0]}"
        else:
            return f"Skill: {', '.join(cleaned_skills)}"
        
    def _create_combined_embedding(self, title_emb: np.ndarray,
                                   desc_emb: np.ndarray,
                                   skills_emb: np.ndarray,
                                   weights: dict) -> np.ndarray:
        """
            Create weighted combination of different embeddings.
        """
        
        try:
            combined = (
                weights['title'] * title_emb +
                weights['description'] * desc_emb +
                weights['skills'] * skills_emb
            )
            
            norm = np.linalg.norm(combined)
            if norm > 0:
                combined = combined / norm
            
            return combined.astype(np.float32)
        except Exception as e:
            logger.error(f"Error creating combined embedding: {e}")
            return np.zeros(self.dimension, dtype=np.float32)
        
    def get_embedding_stats(self) -> dict:
        return {
            'model_name': self.model_name,
            'dimension': self.dimension,
            'model_loaded': self._model is not None
        }

embedding_service = EmbeddingService()

def encode_text(text: str) -> np.ndarray:
    return embedding_service.encode_text(text)

def encodee_skills(skills: List[str]) -> np.ndarray:
    return embedding_service.encode_skills(skills)

def calculate_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    return embedding_service.calculate_similarity(emb1, emb2)
        