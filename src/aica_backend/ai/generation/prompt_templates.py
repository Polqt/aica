from typing import List, Dict, Any

class PromptTemplates:
    def create_job_match_prompt(self,
                                user_skills: List[str],
                                job_title: str,
                                company_name: str,
                                required_skills: List[str],
                                preferred_skills: List[str],
                                job_description: str,
                                similarity_score: float) -> str:
        
        user_skills_text = ", ".join(user_skills) if user_skills else "No skills listed"
        required_skills_text = ", ".join(required_skills) if required_skills else "Not specified"
        preferred_skills_text = ", ".join(preferred_skills) if preferred_skills else "Not specified"
        
        job_desc_truncated = job_description[:500] + "..." if len(job_description) > 500 else job_description
        
        prompt = f"""
            You are an expert career counselor and job matching specialist in tech industry. Analyze the compatibility
            between a candidate's skills and a job posting.
            
            ### Candidate Profile:
            **Skills:** {user_skills_text}
            
            ## Job Posting:
            **Position:** {job_title}
            **Company:** {company_name}
            **Required Skills:** {required_skills_text}
            **Preferred Skills:** {preferred_skills_text}
            **Job Description:** {job_desc_truncated}
            **AI Similarity Score:** {similarity_score:.1%}
            
            ## Analyze Task:
            Provide a comprehensive analysis of why this job matches (or doesn't match) the candidate's profile. Your analysis should be professional,
            specific, and actionable.
            
            ## Response Format:
            **Match Assessment:**
            [Provide an overall assessment of the match quality]
            
            **Matching Skills:**
            - [List specific skills that align between candidate and job requirements]
            - [Explain how each matching skills is relevant to the role]
            
            **Skill Gaps:**
            - [Identify skills required by the job that the candidate lacks]
            - [Prioritize which gaps are most critical to address]
            
            **Recommendations:**
            [Provide specific, actionable advice for the candidate, including:]
            - How to leverage existing skills
            - Which missing skills to prioritize learning
            - Strategies to strengthen the application
            
            **Match Confidence:** [Rate the match quality on a scale from Weak to Excellent]
            
            Keep your response concise but thorough, focusin on practical insights that will help the candidate make informed decisions.
        """
        
        return prompt
    
    def create_skills_gap_prompt(self,
                                user_skills: List[str],
                                job_title: str,
                                required_skills: List[str],
                                preferred_skills: List[str]) -> str:
        
        user_skills_text = ", ".join(user_skills) if user_skills else "No skills listed"
        required_skills_text = ", ".join(required_skills) if required_skills else "Not specified"
        preferred_skills_text = ", ".join(preferred_skills) if preferred_skills else "Not specified"
        
        prompt = f"""
            You are a skills development advisor. Analyze the skill gaps between a candidate and a specific job role to create a personalized learning plan.
            
            ### Current Skills:
            {user_skills_text}
            
            ### Target Role:
            **Position:** {job_title}
            **Required Skills:** {required_skills_text}
            **Preferred Skills:** {preferred_skills_text}
            
            ## Analysis Task:
            Conduct a thorough skill gap analysis and provide a structured learning path.
            
            ## Response Format:
            **Skill Gap Analysis:**
            [Comprehensive overview of the gaps between current skills and job requirements]
            
            **Critical Missing Skills:**
            - [List most important missing skills in order of priority]
            - [Explain why each skill is important for the role]
            
            **Skill Development Priority:**
            1. **High Priority:** [Skills essential for basic job performance]
            2. **Medium Priority:** [Skills that would enhance performance]
            3. **Low Priority:** [Nice-to-have skills for career advancement]
            
            **Learning Path:**
            - **Phase 1 (0-2 months):** [Foundational skills to develop first]
            - **Phase 2 (2-4 months):** [Intermediate skills building on foundation]
            - **Phase 3 (4-6 months):** [Advanced skills for role mastery]

            **Learning Resources & Strategies:**
            - [Suggest specific types of courses, certifications, or projects]
            - [Recommend practice methods for each skill area]
            
            **Timeline Estimate:** [Realistic timeframe to become job-ready]
            
            Focus on creating a practical, achievable learning plan that builds systematically toward the target role.
        """
        return prompt