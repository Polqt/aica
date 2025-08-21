import logging
import numpy as np

from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    """
        Handles storage and retrieval of embeddings for jobs and user profiles.
    """
    
    def __init__(self):
        self.dimension = settings.EMBEDDING_DIMENSION
        self.similarity_threshold = settings.VECTOR_SIMILARITY_THRESHOLD
    
    async def store_job_embeddings(self, session: AsyncSession,
                                   job_id: int, embeddings: Dict[str, np.ndarray]) -> bool:
        
        """
            Store job embeddings to the database
        """
        
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
        """
            Store user profile skills embedding
        """
        
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
                'skills_emb': skills_embedding
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
        
        """
            Find jobs similar to user skills using vector similarity.
        """
        
        try:
            threshold = similarity_threshold or self.similarity_threshold
            user_emb_list = user_skills_embedding.tolist()
            
            query = text("""
                            SELECT
                                jp.id
                                jp.title,
                                jp.company_name,
                                jp.location,
                                jp.description,
                                jp.required_skills,
                                jp.preferred_skills,
                                jp.salary_range,
                                jp.job_typem
                                jp.experience_levelm
                                jp.posted_date,
                                
                                1 - (jp.skills_embedding <=> :user_embedding::vector) as skills_similarity,
                                1 - (jp.description_embedding <=> :user_embedding::vector) as description_similarity,
                                (
                                    0.7 * (1 - (jp.skills_embedding <=> :user_embedding:vector)) +
                                    0.3 * (1 - (jp.description_embedding <=> :user_embedding:vector))
                                ) as combined_similarity
                            FROM job_postings AS jp
                            WHERE
                                jp.skills_embedding IS NOT NULL 
                                    AND jp.is_active = true 
                                    AND (
                                        1 - (jp.skills_embedding <=> :user_embedding::vector) >= :threshold
                                        OR 1 - (jp.description_embedding <=> :user_embedding::vector) >= : threshold
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
    
    async def find_similar_users(self, session: AsyncSession,
                                job_skills_embedding: np.ndarray,
                                limit: int = 20) -> List[Dict[str, Any]]:
        
        """
            Find users with similar skills to a job posting.
        """
        
    async def get_job_recommendations_by_filters(self, session: AsyncSession, 
                                                user_skills_embedding: np.ndarray,
                                                filters: Dict[str, Any],
                                                limit: int = 20) -> List[Dict[str, Any]]:
        
        """
            Get job recommendations with additional filters
        """
        
        try:
            user_emb_list = user_skills_embedding.tolist()
            
            where_conditions = ["jp.skills_embedding IS NOT NULL", "jp_is_active = true"]
            query_params = {
                'user_embedding': user_emb_list,
                'threshold': self.similarity_threshold,
                'limit': limit
            }
            
            if filters.get('location'):
                where_conditions.append("LOWER(jp.location) LIKE LOWER(:location)")
                query_params['location'] = f"%{filters['location']}%"
            
            if filters.get('job_type'):
                where_conditions.append("jp.job_type = :job_type")
                query_params['job_type'] = filters['job_type']
            
            if filters.get('experience_level'):
                where_conditions.append("jp.experience_level = :experience_level")
                query_params['experience_level'] = filters['experience_level']
            
            if filters.get('min_salary'):
                where_conditions.append("jp.salary_min >= :min_salary")
                query_params['min_salary'] = filters['min_salary']
            
            if filters.get('max_salary'):
                where_conditions.append("jp.salary_max <= :max_salary")
                query_params['max_salary'] = filters['max_salary']
            
            where_clause = " AND ".join(where_conditions)
            
            query = text(f"""
                            SELECT 
                                jp.id,
                                jp.title,
                                jp.company_name,
                                jpb.description,
                                jp.required_skills,
                                jp.preferred_skills,
                                jp.salary_range,
                                jp.job_type,
                                jp.experience_level,
                                jp.posted_date,
                                1 - (jp.skills_embedding <=> :user_embedding::vector) as skills_similarity,
                                1 - (jp.description_embedding <=> :user_embedding::vector) as description_similarity,
                                (
                                    0.7 * (1 - (jp.skills_embedding <=> :user_embedding::vector)) +
                                    0.3 * (1 - (jp.description_embedding <=> :user_embedding::vector))
                                ) AS combined_similarity
                            FROM job_postings AS jp
                            WHERE {where_clause}
                                AND 1 - (jp.skills_embedding <=> :user_embedding::vector) >= :threshold
                            ORDER BY combined_similarity DESC
                            LIMIT :limit
                        """)    
            results = await session.execute(query, query_params)
            
            jobs = []
            for row in results.fetchall():
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
            logger.error(f"Error converting user skills embedding to list: {e}")
            return []
        
    async def bulk_store_job_embeddings(self,
                                        session: AsyncSession,
                                        job_embeddings: List[Dict[str, Any]]) -> int:
        """
            Bulk store mebeddings for multiple jobs
        """
        
        success_count = 0
        
        for job_data in job_embeddings:
            try:
                job_id = job_data['job_id']
                embeddings = job_data['embeddings']
                
                success = await self.store_job_embeddings(session, job_id, embeddings)
                
                if success:
                    success_count += 1
            except Exception as e:
                logger.error(f"Error in bulk store for job {job_data.get('job_id', 'unknown')}")
                continue    
    
    async def create_vector_indexes(self, session: AsyncSession) -> bool:
        """
            Create vector indexes for optimal similarity search performance
        """
        
        try:
            # Create indexes for job postings
            await session.execute(text("""
                CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_skills_embedding
                ON job_postings USING ivfflag (skills_embedding vector_cosine_ops)
                WITH (lists = 100)
            """))
            
            await session.execute(text("""
                CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_description_embedding
                ON job_postings USING ivfflag (description_embedding vector_cosine_ops)
                WITH (lists = 100)
            """))
            
            # Create index for user profiles
            await session.execute(text("""
                CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_skills_embedding
                ON user_profiles USING ivfflat (skills_embedding vector_cosine_ops)
                WITH (lists = 100)                        
            """))
            
            await session.commit()
            logger.info("Vector indexes created successfully")
            return True
        except Exception as e:
            logger.error(f"Errorr creating vector indexes: {str(e)}")
            await session.rollback()
            return False

vector_store = VectorStore()

async def store_job_embeddings(session: AsyncSession, job_id: int, embeddings: Dict[str, np.ndarray]) -> bool:
    return await vector_store.store_job_embeddings(session, job_id, embeddings)

async def find_similar_jobs(session: AsyncSession, user_skills_embedding: np.ndarray,
                            limit: int = 20) -> List[Dict[str, Any]]:
    return await vector_store.find_similar_jobs(session, user_skills_embedding, limit)