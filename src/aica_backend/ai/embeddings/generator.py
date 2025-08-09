import numpy as np
from typing import List, Optional, Dict, Any
from sentence_transformers import SentenceTransformer
import logging
from ...core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self._model = None
        self._load_model()
    
    def _load_model(self):
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {str(e)}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return np.zeros(self.get_embedding_dimension())
            
        try:
            cleaned_text = self._preprocess_text(text)

            embedding = self._model.encode(cleaned_text, convert_to_numpy=True)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            return np.zeros(self.get_embedding_dimension())
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        if not texts:
            return []
            
        try:
            cleaned_texts = [self._preprocess_text(text) for text in texts]

            valid_texts = [text for text in cleaned_texts if text.strip()]
            
            if not valid_texts:
                logger.warning("No valid texts to embed")
                return [np.zeros(self.get_embedding_dimension()) for _ in texts]

            embeddings = self._model.encode(valid_texts, convert_to_numpy=True)

            result = []
            valid_idx = 0
            for original_text in cleaned_texts:
                if original_text.strip():
                    result.append(embeddings[valid_idx])
                    valid_idx += 1
                else:
                    result.append(np.zeros(self.get_embedding_dimension()))
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {str(e)}")
            return [np.zeros(self.get_embedding_dimension()) for _ in texts]
    
    def generate_skill_embedding(self, skills: List[str]) -> np.ndarray:
        """
        Generate embedding for a list of skills
        
        Args:
            skills: List of skill names
            
        Returns:
            Combined embedding representing the skill set
        """
        if not skills:
            return np.zeros(self.get_embedding_dimension())
        
        # Create skill text representation
        skill_text = ", ".join(skills)
        skill_description = f"Professional skills: {skill_text}"
        
        return self.generate_embedding(skill_description)
    
    def generate_job_embedding(self, job_data: Dict[str, Any]) -> np.ndarray:
        """
        Generate comprehensive embedding for a job posting
        
        Args:
            job_data: Dictionary containing job information
            
        Returns:
            Job embedding
        """
        try:
            # Combine relevant job fields into a comprehensive text
            text_parts = []
            
            # Job title (weighted more heavily)
            if job_data.get('job_title'):
                text_parts.append(f"Job Title: {job_data['job_title']}")
            
            # Company and location
            if job_data.get('company_name'):
                text_parts.append(f"Company: {job_data['company_name']}")
            
            if job_data.get('location'):
                text_parts.append(f"Location: {job_data['location']}")
            
            # Skills
            if job_data.get('all_skills'):
                skills_text = ", ".join(job_data['all_skills'])
                text_parts.append(f"Required Skills: {skills_text}")
            
            # Job details
            if job_data.get('work_type'):
                text_parts.append(f"Work Type: {job_data['work_type']}")
            
            if job_data.get('employment_type'):
                text_parts.append(f"Employment: {job_data['employment_type']}")
            
            if job_data.get('experience_level'):
                text_parts.append(f"Experience Level: {job_data['experience_level']}")
            
            # Description (limited to avoid overwhelming)
            if job_data.get('full_text'):
                description = job_data['full_text'][:1000]  # Limit length
                text_parts.append(f"Description: {description}")
            
            # Combine all parts
            combined_text = " | ".join(text_parts)
            
            return self.generate_embedding(combined_text)
            
        except Exception as e:
            logger.error(f"Failed to generate job embedding: {str(e)}")
            return np.zeros(self.get_embedding_dimension())
    
    def generate_profile_embedding(self, profile_data: Dict[str, Any]) -> np.ndarray:
        """
        Generate comprehensive embedding for a user profile
        
        Args:
            profile_data: Dictionary containing profile information
            
        Returns:
            Profile embedding
        """
        try:
            text_parts = []
            
            # Professional title
            if profile_data.get('professional_title'):
                text_parts.append(f"Professional Title: {profile_data['professional_title']}")
            
            # Summary
            if profile_data.get('summary'):
                text_parts.append(f"Professional Summary: {profile_data['summary']}")
            
            # Skills
            if profile_data.get('skills'):
                skills_text = ", ".join([skill['name'] for skill in profile_data['skills']])
                text_parts.append(f"Skills: {skills_text}")
            
            # Experience
            if profile_data.get('experiences'):
                for exp in profile_data['experiences'][:3]:  # Limit to recent experiences
                    exp_text = f"Experience: {exp.get('job_title', '')} at {exp.get('company_name', '')}"
                    if exp.get('description'):
                        exp_text += f" - {exp['description'][:200]}"
                    text_parts.append(exp_text)
            
            # Education
            if profile_data.get('educations'):
                for edu in profile_data['educations'][:2]:  # Limit to 2 most relevant
                    edu_text = f"Education: {edu.get('degree', '')} in {edu.get('field_of_study', '')} from {edu.get('institution_name', '')}"
                    text_parts.append(edu_text)
            
            # Combine all parts
            combined_text = " | ".join(text_parts)
            
            return self.generate_embedding(combined_text)
            
        except Exception as e:
            logger.error(f"Failed to generate profile embedding: {str(e)}")
            return np.zeros(self.get_embedding_dimension())
    
    def _preprocess_text(self, text: str) -> str:
        if not text:
            return ""
        cleaned = text.strip()

        cleaned = " ".join(cleaned.split())

        if len(cleaned) > 5000:
            cleaned = cleaned[:5000] + "..."
        
        return cleaned
    
    def get_embedding_dimension(self) -> int:
        if self._model is None:
            return settings.EMBEDDING_DIMENSION
        return self._model.get_sentence_embedding_dimension()
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        try:
            # Normalize vectors
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Calculate cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            
            # Ensure result is between 0 and 1
            similarity = max(0.0, min(1.0, similarity))
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {str(e)}")
            return 0.0

_embedding_generator = None

def get_embedding_generator() -> EmbeddingGenerator:
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator
