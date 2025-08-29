from typing import List, Dict, Any, Optional
import logging
import numpy as np

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.dimension = settings.EMBEDDING_DIMENSION
        self.similarity_threshold = settings.VECTOR_SIMILARITY_THRESHOLD

    async def store_job_embeddings(self, session: AsyncSession,
                                   job_id: int, embeddings: Dict[str, np.ndarray]) -> bool:
        try:
            skills_embedding = embeddings.get('skills', np.zeros(self.dimension)).tolist()
            description_embedding = embeddings.get('description', np.zeros(self.dimension)).tolist()
            query = text("""
                            UPDATE job_postings
                            SET skills_embedding = :skills_emb::vector,
                                description_embedding = :desc_emb::vector,
                                updated_at = NOW()
                            WHERE id = :job_id
                        """)
            await session.execute(query, {
                'job_id': job_id,
                'skills_emb': skills_embedding,
                'desc_emb': description_embedding,
            })
            await session.commit()
            logger.info(f"Stored embeddings for job ID {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing job embeddings for ID {job_id}: {e}")
            await session.rollback()
            return False

    async def store_user_profile_embedding(self, session: AsyncSession,
                                           user_id: int, skills_embedding: np.ndarray) -> bool:
        try:
            skills_emb_list = skills_embedding.tolist()
            query = text("""
                            UPDATE user_profiles
                            SET skills_embedding = :skills_emb::vector,
                                updated_at = NOW()
                            WHERE user_id = :user_id
                        """)
            await session.execute(query, {
                'user_id': user_id,
                'skills_emb': skills_emb_list
            })
            await session.commit()
            logger.info(f"Stored user profile embedding for user ID {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing user profile embedding for user ID {user_id}: {e}")
            await session.rollback()
            return False

    async def find_similar_jobs(self, session: AsyncSession,
                                user_skills_embedding: np.ndarray,
                                limit: int = 20,
                                similarity_threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        try:
            threshold = similarity_threshold or self.similarity_threshold
            user_emb_list = user_skills_embedding.tolist()
            query = text("""
                            SELECT
                                jp.id,
                                jp.title,
                                jp.company_name,
                                jp.location,
                                jp.description,
                                jp.required_skills,
                                jp.preferred_skills,
                                jp.salary_range,
                                jp.job_type,
                                jp.experience_level,
                                jp.posted_date,
                                1 - (jp.skills_embedding <=> :user_embedding::vector) AS skills_similarity,
                                1 - (jp.description_embedding <=> :user_embedding::vector) AS description_similarity,
                                (
                                    0.7 * (1 - (jp.skills_embedding <=> :user_embedding::vector)) +
                                    0.3 * (1 - (jp.description_embedding <=> :user_embedding::vector))
                                ) AS combined_similarity
                            FROM job_postings AS jp
                            WHERE
                                jp.skills_embedding IS NOT NULL 
                                AND jp.is_active = true 
                                AND (
                                    1 - (jp.skills_embedding <=> :user_embedding::vector) >= :threshold
                                    OR 1 - (jp.description_embedding <=> :user_embedding::vector) >= :threshold
                                )
                            ORDER BY combined_similarity DESC
                            LIMIT :limit
                        """)
            result = await session.execute(query, {
                'user_embedding': user_emb_list,
                'threshold': threshold,
                'limit': limit
            })
            jobs = []
            for row in result.fetchall():
                job_data = {
                    'id': row.id,
                    'title': row.title,
                    'company_name': row.company_name,
                    'location': row.location,
                    'description': row.description,
                    'required_skills': row.required_skills or [],
                    'preferred_skills': row.preferred_skills or [],
                    'salary_range': row.salary_range,
                    'job_type': row.job_type,
                    'experience_level': row.experience_level,
                    'posted_date': row.posted_date,
                    'similarity_scores': {
                        'skills_similarity': float(row.skills_similarity),
                        'description_similarity': float(row.description_similarity),
                        'combined_similarity': float(row.combined_similarity)
                    }
                }
                jobs.append(job_data)
            logger.info(f"Found {len(jobs)} similar jobs for user skills embedding")
            return jobs
        except Exception as e:
            logger.error(f"Error finding similar jobs: {e}")
            return []

    def find_similar_jobs_sync(self,
                               session,
                               user_skills_embedding: np.ndarray,
                               limit: int = 20,
                               similarity_threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        try:
            threshold = similarity_threshold or self.similarity_threshold
            user_emb_list = user_skills_embedding.tolist()
            query = text("""
                            SELECT
                                jp.id,
                                jp.title,
                                jp.company_name,
                                jp.location,
                                jp.description,
                                jp.required_skills,
                                jp.preferred_skills,
                                jp.salary_range,
                                jp.job_type,
                                jp.experience_level,
                                jp.posted_date,
                                1 - (jp.skills_embedding <=> :user_embedding::vector) AS skills_similarity,
                                1 - (jp.description_embedding <=> :user_embedding::vector) AS description_similarity,
                                (
                                    0.7 * (1 - (jp.skills_embedding <=> :user_embedding::vector)) +
                                    0.3 * (1 - (jp.description_embedding <=> :user_embedding::vector))
                                ) AS combined_similarity
                            FROM job_postings AS jp
                            WHERE
                                jp.skills_embedding IS NOT NULL 
                                AND jp.is_active = true 
                                AND (
                                    1 - (jp.skills_embedding <=> :user_embedding::vector) >= :threshold
                                    OR 1 - (jp.description_embedding <=> :user_embedding::vector) >= :threshold
                                )
                            ORDER BY combined_similarity DESC
                            LIMIT :limit
                        """)
            result = session.execute(query, {
                'user_embedding': user_emb_list,
                'threshold': threshold,
                'limit': limit
            })
            jobs = []
            for row in result.fetchall():
                job_data = {
                    'id': row.id,
                    'title': row.title,
                    'company_name': row.company_name,
                    'location': row.location,
                    'description': row.description,
                    'required_skills': row.required_skills or [],
                    'preferred_skills': row.preferred_skills or [],
                    'salary_range': row.salary_range,
                    'job_type': row.job_type,
                    'experience_level': row.experience_level,
                    'posted_date': row.posted_date,
                    'similarity_scores': {
                        'skills_similarity': float(row.skills_similarity),
                        'description_similarity': float(row.description_similarity),
                        'combined_similarity': float(row.combined_similarity)
                    }
                }
                jobs.append(job_data)
            return jobs
        except Exception as e:
            logger.error(f"Error finding similar jobs (sync): {e}")
            return []

vector_store = VectorStore()


