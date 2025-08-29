from typing import List, Dict, Any, Optional
import logging
import numpy as np
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ...core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.dimension = settings.EMBEDDING_DIMENSION
        self.similarity_threshold = settings.VECTOR_SIMILARITY_THRESHOLD

        # Connection pooling for better performance
        self._engine = None
        self._session_factory = None
        self._setup_connection_pool()

    def _setup_connection_pool(self):
        """Setup optimized database connection pool for vector operations."""
        try:
            self._engine = create_async_engine(
                settings.DATABASE_URL,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=3600,
                echo=False
            )
            self._session_factory = async_sessionmaker(
                self._engine,
                expire_on_commit=False
            )
            logger.info("Vector store connection pool initialized")
        except Exception as e:
            logger.error(f"Error setting up connection pool: {e}")

    @asynccontextmanager
    async def _get_session(self):
        """Context manager for database sessions."""
        if not self._session_factory:
            raise Exception("Database connection not initialized")

        session = self._session_factory()
        try:
            yield session
        finally:
            await session.close()

    async def health_check(self) -> Dict[str, Any]:
        """Check vector store health and performance."""
        try:
            async with self._get_session() as session:
                # Test basic connectivity
                query = text("SELECT 1 as test")
                result = await session.execute(query)
                row = result.fetchone()

                # Check pgvector extension
                query = text("SELECT * FROM pg_extension WHERE extname = 'vector'")
                result = await session.execute(query)
                pgvector_installed = result.fetchone() is not None

                return {
                    "status": "healthy" if pgvector_installed else "degraded",
                    "pgvector_installed": pgvector_installed,
                    "connection_pool_size": 10,  # From pool_size setting
                    "embedding_dimension": self.dimension
                }
        except Exception as e:
            logger.error(f"Vector store health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    async def store_job_embeddings_batch(self, session: AsyncSession,
                                         job_embeddings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Batch store multiple job embeddings for better performance.

        Args:
            session: Database session
            job_embeddings: List of dicts with 'job_id' and 'embeddings' keys

        Returns:
            Success/failure statistics
        """
        try:
            success_count = 0
            failure_count = 0

            for job_data in job_embeddings:
                job_id = job_data['job_id']
                embeddings = job_data['embeddings']

                success = await self.store_job_embeddings(session, job_id, embeddings)
                if success:
                    success_count += 1
                else:
                    failure_count += 1

            return {
                "total_processed": len(job_embeddings),
                "successful": success_count,
                "failed": failure_count,
                "success_rate": success_count / len(job_embeddings) if job_embeddings else 0
            }

        except Exception as e:
            logger.error(f"Error in batch job embedding storage: {e}")
            return {
                "total_processed": len(job_embeddings),
                "successful": 0,
                "failed": len(job_embeddings),
                "error": str(e)
            }

    async def create_performance_indexes(self, session: AsyncSession) -> bool:
        """
        Create optimized indexes for vector similarity search performance.
        """
        try:
            # Create vector indexes for better similarity search performance
            indexes = [
                """
                CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_skills_embedding
                ON job_postings USING ivfflat (skills_embedding vector_cosine_ops)
                WITH (lists = 100);
                """,
                """
                CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_description_embedding
                ON job_postings USING ivfflat (description_embedding vector_cosine_ops)
                WITH (lists = 100);
                """,
                """
                CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_skills_embedding
                ON user_profiles USING ivfflat (skills_embedding vector_cosine_ops)
                WITH (lists = 50);
                """
            ]

            for index_sql in indexes:
                try:
                    await session.execute(text(index_sql))
                    logger.info("Created vector performance index")
                except Exception as e:
                    logger.warning(f"Index creation failed (may already exist): {e}")

            await session.commit()
            logger.info("Vector performance indexes created successfully")
            return True

        except Exception as e:
            logger.error(f"Error creating performance indexes: {e}")
            await session.rollback()
            return False

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
