import logging 
import numpy as np

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional

from ...core.config import settings
from ..interfaces import VectorStoreInterface

logger = logging.getLogger(__name__)

class PgVectorStore(VectorStoreInterface):
    
    def __init__(self):
        super.dimension = settings.EMBEDDING_DIMENSION
        super.similarity_threshold = settings.VECTOR_SIMILARITY_THRESHOLD
        
    
    async def store_job_embedding(self, session, job_id, embeddings: Dict[str, np.ndarray]) -> bool:
        try:
            skills_emb = embeddings.get('skills', np.zeros(self.dimension))
            desc_emb = embeddings.get('description', np.zeros(self.dimension))
            
            query = text("""
                UPDATE job_postings 
                SET 
                    skills_embedding = :skills_emb::vector,
                    description_embedding = :desc_emb::vector,
                    status = 'embedded',
                    updated_at = NOW()
                WHERE id = :job_id
            """)
            
            await session.execute(query, {
                'job_id': job_id,
                'skills_emb': skills_emb.tolist(),
                'desc_emb': desc_emb.tolist()
            })
            
            await session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to store embeddings for job {job_id}: {e}")
            await session.rollback()
            return False
    
    async def find_similar_jobs(self, session: AsyncSession, query_embedding: np.ndarray, limit: int = 20, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            where_conditions = [
                "jp.skills_embedding IS NOT NULL",
                "jp.is_active = true"
            ]
            params = {
                'query_emb': query_embedding.tolist(),
                'threshold': self.similarity_threshold,
                'limit': limit
            }
            
            if filters:
                if filters.get('location'):
                    where_conditions.append("LOWER(jp.location) ILIKE LOWER(:location)")
                    params['location'] = f"%{filters['location']}%"
                
                if filters.get('job_type'):
                    where_conditions.append("jp.employment_type = :job_type")
                    params['job_type'] = filters['job_type']
                
                if filters.get('experience_level'):
                    where_conditions.append("jp.experience_level = :experience_level")
                    params['experience_level'] = filters['experience_level']
            
            where_clause = " AND ".join(where_conditions)
            
            query = text(f"""
                SELECT 
                    jp.id,
                    jp.job_title,
                    jp.company_name,
                    jp.location,
                    jp.employment_type,
                    jp.experience_level,
                    jp.technical_skills,
                    jp.salary_min,
                    jp.salary_max,
                    jp.posting_date,
                    1 - (jp.skills_embedding <=> :query_emb::vector) as similarity_score
                FROM job_postings jp
                WHERE {where_clause}
                    AND 1 - (jp.skills_embedding <=> :query_emb::vector) >= :threshold
                ORDER BY similarity_score DESC
                LIMIT :limit
            """)
            
            result = await session.execute(query, params)
            
            jobs = []
            for row in result.fetchall():
                jobs.append({
                    'id': row.id,
                    'title': row.job_title,
                    'company': row.company_name,
                    'location': row.location,
                    'employment_type': row.employment_type,
                    'experience_level': row.experience_level,
                    'skills': row.technical_skills or [],
                    'salary_range': {
                        'min': row.salary_min,
                        'max': row.salary_max
                    },
                    'posting_date': row.posting_date,
                    'similarity_score': float(row.similarity_score)
                })
            
            logger.info(f"Found {len(jobs)} similar jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error finding similar jobs: {e}")
            return []
    
    async def store_user_profile_embedding(
        self, 
        session: AsyncSession, 
        user_id: int, 
        skills_embedding: np.ndarray
    ) -> bool:
        """Store user profile embedding."""
        try:
            query = text("""
                UPDATE user_profiles 
                SET 
                    skills_embedding = :skills_emb::vector,
                    updated_at = NOW()
                WHERE user_id = :user_id
            """)
            
            await session.execute(query, {
                'user_id': user_id,
                'skills_emb': skills_embedding.tolist()
            })
            
            await session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to store user embedding for {user_id}: {e}")
            await session.rollback()
            return False
    
    async def batch_store_embeddings(
        self, 
        session: AsyncSession, 
        job_embeddings: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Bulk store embeddings for multiple jobs."""
        success_count = 0
        error_count = 0
        
        for job_data in job_embeddings:
            try:
                success = await self.store_job_embedding(
                    session, 
                    job_data['job_id'], 
                    job_data['embeddings']
                )
                if success:
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                logger.error(f"Error in batch store: {e}")
                error_count += 1
        
        return {
            'successful': success_count,
            'failed': error_count,
            'total': len(job_embeddings)
        }
        