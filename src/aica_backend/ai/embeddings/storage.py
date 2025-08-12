import faiss
import numpy as np
import pickle
import os
from typing import List, Optional, Tuple, Dict, Any
import logging
from ...core.config import settings

logger = logging.getLogger(__name__)

class VectorStorage:
    def __init__(self, index_path: str = "data/vectors", dimension: int = None):
        self.index_path = index_path
        self.dimension = dimension or settings.EMBEDDING_DIMENSION

        self.index = None
        self.metadata = {}
        self.id_mapping = {}

        os.makedirs(index_path, exist_ok=True)

        self._load_index()
    
    def _load_index(self):
        index_file = os.path.join(self.index_path, "faiss_index")
        metadata_file = os.path.join(self.index_path, "metadata.pkl")
        mapping_file = os.path.join(self.index_path, "id_mapping.pkl")
        
        try:
            if os.path.exists(index_file) and os.path.exists(metadata_file):
                self.index = faiss.read_index(index_file)

                with open(metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)

                if os.path.exists(mapping_file):
                    with open(mapping_file, 'rb') as f:
                        self.id_mapping = pickle.load(f)
                
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                self._create_new_index()
                
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {str(e)}")
            self._create_new_index()
    
    def _create_new_index(self):
        try:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = {}
            self.id_mapping = {}
            
            logger.info(f"Created new FAISS index with dimension {self.dimension}")
        except Exception as e:
            logger.error(f"Failed to create FAISS index: {str(e)}")
            raise
    
    def save_index(self):
        try:
            index_file = os.path.join(self.index_path, "faiss_index")
            metadata_file = os.path.join(self.index_path, "metadata.pkl")
            mapping_file = os.path.join(self.index_path, "id_mapping.pkl")
            
            # Save FAISS index
            faiss.write_index(self.index, index_file)
            
            # Save metadata
            with open(metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
            
            # Save ID mapping
            with open(mapping_file, 'wb') as f:
                pickle.dump(self.id_mapping, f)
            
            logger.info(f"Saved FAISS index with {self.index.ntotal} vectors")
            
        except Exception as e:
            logger.error(f"Failed to save FAISS index: {str(e)}")
            raise
    
    def add_vector(self, vector_id: int, embedding: np.ndarray, metadata: Dict[str, Any] = None):
        try:
            if embedding.ndim == 1:
                embedding = embedding.reshape(1, -1)

            normalized_embedding = self._normalize_vector(embedding)

            faiss_idx = self.index.ntotal
            self.index.add(normalized_embedding.astype(np.float32))
            
            self.id_mapping[faiss_idx] = vector_id
            self.metadata[vector_id] = metadata or {}
            
            logger.debug(f"Added vector {vector_id} to index")
            
        except Exception as e:
            logger.error(f"Failed to add vector {vector_id}: {str(e)}")
            raise
    
    def add_vectors_batch(self, vector_data: List[Tuple[int, np.ndarray, Dict[str, Any]]]):
        try:
            if not vector_data:
                return
            
            # Prepare embeddings
            embeddings = []
            for vector_id, embedding, metadata in vector_data:
                if embedding.ndim == 1:
                    embedding = embedding.reshape(1, -1)
                normalized_embedding = self._normalize_vector(embedding)
                embeddings.append(normalized_embedding)
            
            # Stack all embeddings
            batch_embeddings = np.vstack(embeddings).astype(np.float32)
            
            # Add to FAISS index
            start_idx = self.index.ntotal
            self.index.add(batch_embeddings)
            
            # Store mappings and metadata
            for i, (vector_id, _, metadata) in enumerate(vector_data):
                faiss_idx = start_idx + i
                self.id_mapping[faiss_idx] = vector_id
                self.metadata[vector_id] = metadata or {}
            
            logger.info(f"Added {len(vector_data)} vectors to index")
            
        except Exception as e:
            logger.error(f"Failed to add vector batch: {str(e)}")
            raise
    
    def search_similar(self, query_embedding: np.ndarray, k: int = 10, threshold: float = None) -> List[Tuple[int, float]]:
        try:
            if self.index.ntotal == 0:
                return []
            
            # Normalize query vector
            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            normalized_query = self._normalize_vector(query_embedding)
            
            # Search in FAISS index
            distances, indices = self.index.search(normalized_query.astype(np.float32), k)
            
            # Convert L2 distances to cosine similarities
            results = []
            for distance, faiss_idx in zip(distances[0], indices[0]):
                if faiss_idx == -1:  # No more results
                    break
                
                # Convert L2 distance to cosine similarity
                similarity = max(0.0, 1.0 - (distance / 2.0))
                
                # Apply threshold if specified
                if threshold is not None and similarity < threshold:
                    continue
                
                # Get original vector ID
                vector_id = self.id_mapping.get(faiss_idx)
                if vector_id is not None:
                    results.append((vector_id, float(similarity)))
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search similar vectors: {str(e)}")
            return []
    
    def get_vector_metadata(self, vector_id: int) -> Optional[Dict[str, Any]]:
        return self.metadata.get(vector_id)
    
    def remove_vector(self, vector_id: int):
        try:
            # Find FAISS index for this vector_id
            faiss_idx_to_remove = None
            for faiss_idx, vid in self.id_mapping.items():
                if vid == vector_id:
                    faiss_idx_to_remove = faiss_idx
                    break
            
            if faiss_idx_to_remove is None:
                logger.warning(f"Vector {vector_id} not found in index")
                return
            
            # Rebuild index without this vector
            all_vectors = []
            new_metadata = {}
            new_id_mapping = {}
            
            for faiss_idx in range(self.index.ntotal):
                if faiss_idx != faiss_idx_to_remove:
                    vector = self.index.reconstruct(faiss_idx)
                    vid = self.id_mapping[faiss_idx]
                    
                    all_vectors.append(vector)
                    new_metadata[vid] = self.metadata[vid]
                    new_id_mapping[len(all_vectors) - 1] = vid
            
            # Create new index
            self._create_new_index()
            
            if all_vectors:
                vectors_array = np.vstack(all_vectors).astype(np.float32)
                self.index.add(vectors_array)
            
            self.metadata = new_metadata
            self.id_mapping = new_id_mapping
            
            logger.info(f"Removed vector {vector_id} from index")
            
        except Exception as e:
            logger.error(f"Failed to remove vector {vector_id}: {str(e)}")
            raise
    
    def _normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        """Normalize vector for cosine similarity"""
        norm = np.linalg.norm(vector, axis=1, keepdims=True)
        norm = np.where(norm == 0, 1, norm)  # Avoid division by zero
        return vector / norm
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get storage statistics"""
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "index_path": self.index_path,
            "metadata_count": len(self.metadata),
            "mapping_count": len(self.id_mapping)
        }

_job_storage = None
_profile_storage = None
_skill_storage = None

def get_job_storage() -> VectorStorage:
    """Get global job vector storage instance"""
    global _job_storage
    if _job_storage is None:
        _job_storage = VectorStorage(index_path="data/vectors/jobs")
    return _job_storage

def get_profile_storage() -> VectorStorage:
    """Get global profile vector storage instance"""
    global _profile_storage
    if _profile_storage is None:
        _profile_storage = VectorStorage(index_path="data/vectors/profiles")
    return _profile_storage

def get_skill_storage() -> VectorStorage:
    """Get global skill vector storage instance"""
    global _skill_storage
    if _skill_storage is None:
        _skill_storage = VectorStorage(index_path="data/vectors/skills")
    return _skill_storage
