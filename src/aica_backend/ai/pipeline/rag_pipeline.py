import logging

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..embeddings.embedding_service import embedding_service
from ..embeddings.vector_store import vector_store
from ..generation.llm_service import llm_service

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm_service = llm_service
    
    async def find_matching_jobs(self,
                                session: AsyncSession,
                                user_id: int,
                                user_skills: List[str],
                                filters: Optional[Dict[str, Any]] = None,
                                limit: int = 20,
                                generate_explanation: bool = True) -> Dict[str, Any]:
        
        try:
            start_time = datetime.now()
            
            # Geneate user skills embedding
            logger.info(f"Generating skills embedding for user {user_id}")
            user_skills_embedding = self.embedding_service.encode_skills(user_skills)
            
            # Store/update user embedding in database
            await self.vector_store.store_user_profile_embedding(
                session, 
                user_id,
                user_skills_embedding
            )
            
            # Vector similarity search
            logger.info(f"Searching for similar jobs for user {user_id}")
            if filters:
                matched_jobs = await self.vector_store.get_job_recommendations_by_filters(
                    session,
                    user_skills_embedding,
                    filters,
                    limit
                )
            else:
                matched_jobs = await self.vector_store.find_similar_jobs(
                    session,
                    user_skills_embedding,
                    limit
                )
            
            if not matched_jobs:
                return {
                    "matches": [],
                    "total_matches": 0,
                    "user_skills": user_skills,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "explanation_generated": False
                } 
            
            # Generate explanations for top matches
            explanations = {}
            if generate_explanation:
                logger.info(f"Generating explainations for {len(matched_jobs)} matches")
                explanations = await self._generate_match_explanations(
                    user_skills,
                    matched_jobs[:5]
                )
                
            # Enhance results with explanations
            enhanced_matches = self._enhance_matches_with_explanations(
                matched_jobs,
                explanations
            )   
            
            # Generate overall summary
            summary = None
            if generate_explanation and matched_jobs:
                summary = await self.llm_service
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Job matching pipeline completed in {processing_time:.2f}s")
            
            return {
                "matches": enhanced_matches,
                "total_matches": len(matched_jobs),
                "user_skills": user_skills,
                "summary": summary,
                "processing_time": processing_time,
                "explanations_generated": generate_explanation,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in job matching pipeline: {str(e)}")
            return {
                "matches": [],
                "total_matches": 0,
                "user_skills": user_skills,
                "error": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "explanations_generated": False
            }
    
    async def analyze_job_compatibility(self,
                                        session: AsyncSession,
                                        user_skills: List[str],
                                        job_id: int) -> Dict[str, Any]:
        try:
            # Fetch job details
            job_data = await self._get_job_by_id(session, job_id)
            if not job_data:
                return {
                    "error": "Job not found"
                }
            
            # Generate embeddings
            user_skills_embedding = self.embedding_service.encode_skills(user_skills)
            
            # Calculate similarity
            job_skills_embedding = job_data.get('skills_embedding')
            if job_skills_embedding is None:
                job_embeddings = self.embedding_service.encode_job_description(
                    title=job_data['title'],
                    description=job_data.get['description', ''],
                    required_skills=job_data.get('required_skills', []),
                    preferred_skills=job_data.get('preferred_skills', []),
                )
                job_skills_embedding = job_embeddings['skills']
            
            similarity_scores = {
                'skills_similarity': self.embedding_service.calculate_similarity(
                    user_skills_embedding,
                    job_skills_embedding
                ),
                'combined_similarity': self.embedding_service.calculate_similarity(
                    user_skills_embedding,
                    job_skills_embedding
                )
            }
            
            # Generate comprehensive analysis
            match_explanation = await self.llm_service.generate_job_match_explanation(
                user_skills,
                job_data,
                similarity_scores
            )
            
            skill_gap_analysis = await self.llm_service.generate_skill_gap_analysis(
                user_skills,
                job_data
            )
            
            return {
                "job": job_data,
                "compatibility_score": similarity_scores['combined_similarity'],
                "match_explanation": match_explanation,
                "skill_gap_analysis": skill_gap_analysis,
                "analysis_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in job compatibility analysis: {str(e)}")
            return {
                "error": str(e),
                "analysis_timestamp": datetime.now().isoformat()
            }
        
    
    async def process_job_batch_for_embedding(self,
                                              session: AsyncSession,
                                              job_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
            Process a batch of jobs to generate and store to the embeddings.
        """
        try:
            start_time = datetime.now()
            processed_jobs = []
            
            for job_data in job_batch:
                try:
                    job_id = job_data.get('id')
                    
                    # Generate embeddings for job
                    embeddings = self.embedding_service.encode_job_description(
                        title=job_data.get('title', ''),
                        description=job_data.get('description', ''),
                        required_skills=job_data.get('required_skills', []),
                        preferred_skills=job_data.get('preferred_skills', [])
                    )            
                    
                    success = await self.vector_store.store_job_embeddings(
                        session,
                        job_id,
                        embeddings
                    )
                    
                    if success:
                        processed_jobs.append({
                            'job_id': job_id,
                            'status': 'success',
                            'embeddings_generated': len(embeddings)
                        })
                    else:
                        processed_jobs.append({
                            'job_id': job_id,
                            'status': 'failed',
                            'error': 'Storage field'
                        })
                except Exception as e:
                    processed_jobs.append({
                        'job_id': job_data.get('id', 'unknown'),
                        'status': 'error',
                        'error': str(e)
                    })
                    continue
                
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "total_jobs": len(job_batch),
                "successful": len([j for j in processed_jobs if j['status'] == 'success']),
                "failed": len([j for j in processed_jobs if j['status'] == 'success']),
                "processing_time": processing_time,
                "job_results": processed_jobs
            }
        except Exception as e:
            logger.error(f"Error processing job batch: {str(e)}")
            return {"error": str(e)}
        
    async def _generate_match_explanation(self,
                                          user_skills: List[str],
                                          matched_jobs: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        
        explanations= {}
        
        # Process explanations concurrently
        tasks = []
        for job_data in matched_jobs:
            task = self.llm_service.generate_job_match_explanation(
                user_skills,
                job_data,
                job_data.get('similarity_scores', {})
            )
            tasks.append((job_data['id'], task))
        
        for job_id, task in tasks:
            try:
                explanation = await task 
                explanations[job_id] = explanation
            except Exception as e:
                logger.error(f"Failed to generate explanation foor job  {job_id}: {str(e)}")
                explanations[job_id] = {
                    "error": str(e),
                    "explanation": "Unable to generate explanation at this time",
                    "fallback": True
                }
                
        return explanations
    
    def _enhance_matches_with_explanations(self,
                                           matched_jobs: List[Dict[str, Any]],
                                           explanations: Dict[int, Dict[str, Any]]) -> List[Dict[str, Any]]:
        
        enhanced_matches = []
        
        for job_data in matched_jobs:
            job_id = job_data.get('id')
            enhanced_job = job_data.copy()
            
            if job_id in explanations:
                enhanced_job['ai_explanation'] = explanations[job_id]
            
            enhanced_matches.append(enhanced_job)
        
        return enhanced_matches
    
    async def _get_job_by_id(self, session: AsyncSession, job_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = text("""
                            SELECT id, title, company_name, location, description,
                                required_skills, preferred_skills, salary_range,
                                job_type, experience_level, posted_date,
                                skills_embedding, description_embedding
                            FROM job_postings
                            WHERE id = :job_id AND is_active = true
                        """)
            
            result = await session.execute(query, {"job_id": job_id})
            row = result.fetchone()
            
            if not row:
                return None
            
            return {
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
                'skills_embedding': row.skills_embedding,
                'description_embedding': row.description_embedding
            }
        except Exception as e:
            logger.error(f"Error fetching job by ID {job_id}: {str(e)}")
            return None
        
rag_pipeline = RAGPipeline()

async def find_matching_jobs(session: AsyncSession, user_id: int, user_skills: List[str], 
                            **kwargs) -> Dict[str, Any]:
    return await rag_pipeline.find_matching_jobs(session, user_id, user_skills, **kwargs)

async def analyze_job_compatibility(session: AsyncSession, user_skills: List[str],
                                    job_id: int) -> Dict[str, Any]:
    return await rag_pipeline.analyze_job_compatibility(session, user_skills, job_id)
