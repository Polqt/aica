from typing import Dict, List, Any
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, model_name: str = "llama3:latest"):
        self.model_name = model_name
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        self._initialize()
    
    def _initialize(self):
        try:
            # Initialize embeddings (same as existing system)
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            # Initialize LLM (local Ollama)
            self.llm = Ollama(
                model=self.model_name,
                temperature=0.7,
                base_url="http://localhost:11434"
            )
            
            logger.info("RAG service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {str(e)}")
            # Fallback to basic functionality without LLM
            self.llm = None
    
    def create_job_knowledge_base(self, jobs: List[Dict[str, Any]]) -> bool:
        try:
            documents = []
            
            for job in jobs:
                # Create rich documents from job data
                content = self._format_job_for_rag(job)
                
                doc = Document(
                    page_content=content,
                    metadata={
                        "job_id": job.get("id"),
                        "title": job.get("job_title", ""),
                        "company": job.get("company_name", ""),
                        "location": job.get("location", ""),
                        "experience_level": job.get("experience_level", ""),
                        "work_type": job.get("work_type", "")
                    }
                )
                documents.append(doc)
            
            # Split documents for better retrieval
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            splits = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vectorstore = FAISS.from_documents(splits, self.embeddings)
            
            # Create QA chain
            if self.llm:
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                    return_source_documents=True
                )
            
            logger.info(f"Created knowledge base with {len(documents)} jobs")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create knowledge base: {str(e)}")
            return False
    
    def _format_job_for_rag(self, job: Dict[str, Any]) -> str:
        parts = []
        
        if job.get("job_title"):
            parts.append(f"Job Title: {job['job_title']}")
        
        if job.get("company_name"):
            parts.append(f"Company: {job['company_name']}")
            
        if job.get("location"):
            parts.append(f"Location: {job['location']}")
            
        if job.get("experience_level"):
            parts.append(f"Experience Level: {job['experience_level']}")
            
        if job.get("work_type"):
            parts.append(f"Work Type: {job['work_type']}")
            
        if job.get("employment_type"):
            parts.append(f"Employment Type: {job['employment_type']}")
            
        if job.get("salary_min") and job.get("salary_max"):
            parts.append(f"Salary Range: {job['salary_min']}-{job['salary_max']} {job.get('salary_currency', 'PHP')}")
        
        # The full job description contains all the skills and requirements
        if job.get("full_text"):
            parts.append(f"Job Description: {job['full_text']}")
        
        return "\n\n".join(parts)
    
    def explain_job_match(self, job: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        if not self.qa_chain:
            return "RAG service not available. Please check LLM connection."
        
        try:
            # Format user profile for context
            profile_context = self._format_profile_for_rag(user_profile)
            
            # Create contextual query
            query = f"""
            Based on this user profile:
            {profile_context}
            
            Explain why the job "{job.get('job_title', '')}" at "{job.get('company_name', '')}" 
            would be a good match. Consider:
            1. How the user's skills align with job requirements
            2. Experience level compatibility  
            3. Career growth opportunities
            4. Any skill gaps and learning opportunities
            
            Provide a concise, actionable explanation.
            """
            
            result = self.qa_chain({"query": query})
            return result["result"]
            
        except Exception as e:
            logger.error(f"Failed to explain job match: {str(e)}")
            return f"Unable to generate explanation: {str(e)}"
    
    def analyze_skill_gap(self, job: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        if not self.qa_chain:
            return "RAG service not available."
        
        try:
            profile_context = self._format_profile_for_rag(user_profile)
            
            query = f"""
            Given this user profile:
            {profile_context}
            
            Analyze the skill gaps for the job "{job.get('job_title', '')}" 
            and provide:
            1. Skills the user already has that match the job
            2. Missing skills that would be valuable
            3. Specific learning recommendations 
            4. Priority order for skill development
            
            Focus on actionable advice for career growth.
            """
            
            result = self.qa_chain({"query": query})
            return result["result"]
            
        except Exception as e:
            logger.error(f"Failed to analyze skill gap: {str(e)}")
            return f"Unable to analyze skill gap: {str(e)}"
    
    def generate_career_advice(self, user_profile: Dict[str, Any], target_roles: List[str] = None) -> str:
        if not self.qa_chain:
            return "RAG service not available."
        
        try:
            profile_context = self._format_profile_for_rag(user_profile)
            
            target_context = ""
            if target_roles:
                target_context = f"The user is interested in these roles: {', '.join(target_roles)}"
            
            query = f"""
            Based on this professional profile:
            {profile_context}
            
            {target_context}
            
            Provide career advice including:
            1. Strengths and marketable skills
            2. Recommended career paths
            3. Skills to develop for advancement
            4. Industry trends and opportunities
            5. Next steps for career growth
            
            Keep advice practical and actionable.
            """
            
            result = self.qa_chain({"query": query})
            return result["result"]
            
        except Exception as e:
            logger.error(f"Failed to generate career advice: {str(e)}")
            return f"Unable to generate career advice: {str(e)}"
    
    def _format_profile_for_rag(self, profile: Dict[str, Any]) -> str:
        parts = []
        
        if profile.get("professional_title"):
            parts.append(f"Current Role: {profile['professional_title']}")
        
        if profile.get("summary"):
            parts.append(f"Professional Summary: {profile['summary']}")
        
        # Format experiences
        if profile.get("experiences"):
            exp_texts = []
            for exp in profile["experiences"]:
                exp_text = f"- {exp.get('job_title', '')} at {exp.get('company_name', '')}"
                if exp.get("description"):
                    exp_text += f": {exp['description']}"
                exp_texts.append(exp_text)
            parts.append(f"Work Experience:\n" + "\n".join(exp_texts))
        
        # Format education
        if profile.get("educations"):
            edu_texts = []
            for edu in profile["educations"]:
                edu_text = f"- {edu.get('degree', '')} in {edu.get('field_of_study', '')} from {edu.get('institution_name', '')}"
                edu_texts.append(edu_text)
            parts.append(f"Education:\n" + "\n".join(edu_texts))
        
        # Format skills (RAG will understand these contextually)
        if profile.get("skills"):
            if isinstance(profile["skills"], list):
                skill_names = [skill.get("name", str(skill)) for skill in profile["skills"]]
                parts.append(f"Skills: {', '.join(skill_names)}")
        
        return "\n\n".join(parts)
    
    def get_similar_jobs(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if not self.vectorstore:
            return []
        
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            
            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": getattr(doc, "score", 0.0)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to find similar jobs: {str(e)}")
            return []

_rag_service = None

def get_rag_service() -> RAGService:
    """Get global RAG service instance"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
