"""
Embeddings Module

This module provides a unified interface for text embedding generation and storage.
"""

from .generator import EmbeddingGenerator, get_embedding_generator
from .models import EmbeddingModelManager, get_model_manager
from .storage import VectorStorage, get_job_storage, get_profile_storage, get_skill_storage

__all__ = [
    'EmbeddingGenerator',
    'get_embedding_generator',
    'EmbeddingModelManager', 
    'get_model_manager',
    'VectorStorage',
    'get_job_storage',
    'get_profile_storage', 
    'get_skill_storage'
]
