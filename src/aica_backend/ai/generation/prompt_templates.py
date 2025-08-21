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
    
    def create_multiple_matches_prompt(self,
                                       user_skills: List[str],
                                       matched_jobs: List[Dict[str, Any]]) -> str:
        
        user_skills_text = ", ".join(user_skills) if user_skills else "No skills listed"
        
        jobs_summary = []
        
        for i, job in enumerate(matched_jobs[:5], 1):
            similarity = job.get('similarity_scores', {}).get('combined_simiilarity', 0.0)
            jobs_summary.append(
                f"{i}. {job['title']} at {job['company_name']} - "
                f"(Match: {similarity:.1%}, Location: {job.get('location', 'Not specified')})"
            )
            
            jobs_text  = "\n".join(jobs_summary)
           
        
        
        prompt = f"""
            You are a career strategist analyzing multiple job opportunities for a candidate. Provide insights about their job market position and career opportunities.
            
            ## Candidate Skills:
            {user_skills_text}
            
            ## Matched Job Opportunities:
            {matched_jobs}
            
            ## Analysis Task:
            Provide a comprehensive overview of the gaps between current skills and job requirements.

            ## Response Format:
            **Market Position Summary:**
            [Overview of how the candidate's skills position them in the current job market.]
            
            **Opportunity Analysis:**
            - **Strongest Matches:** [Identify the best 2-3 tech job opportunities that is aligned to user skills.]
            - **Industry Matches:** [What industries are showing interest in these skills]
            - **Geographic Insights:** [Any location-based observations]
            
            **Skill Market Value:**
            - **High-Demand Skills:** [Which of the candidate's skills are most sought after]
            - **Emerging Opportunities:** [New directions these skills could lead to]
            - **Skill Comibations:** [How the candidate's skill mix creates unique value]
            
            **Strategic Recommendations:**
            1. **Short Term (Next 3 months):** [Immediate actions and best opportunities to pursue]
            2. **Medium Term (3-12 months):** [Career development strategies]
            3. **Long Term (1+ years):** [Career advancement pathways]
            
            **Next Steps:**
            [Specific, actionable advice for maximizing these opportunities]
            
            Focus on providing strategic career insights that help the candidate understand their market position and make informed decisions about their career path.
        """
         
        return prompt
    
    def create__career_recommendations_prompt(self,
                                      user_skills: List[str],
                                      current_title: str,
                                      experience_years: int,
                                      job_trends: List[Dict[str, Any]]) -> str:
        
        user_skills_text = ", ".join(user_skills) if user_skills else "No skills listed"
        
        trends_summary = []
        for trend in job_trends[:3]:
            trends_summary.append(
                f"- {trend.get('job_title', 'Unknown')} roles are {trend.get('trend', 'trending')} - "
                f"(Growth: {trend.get('growth_rate', 'N/A')})"
            )
        
        trends_text = "\n".join(trends_summary) if trends_summary else "No trend data available"
        
        prompt = f"""
            You are a senior career advisor providing personalized career development guidance based on skills, experience, and market trends.
            
            ## Current Profile:
            **Current Role:** {current_title or 'Not specified'}
            **Experience:** {experience_years} years
            **Skills:** {user_skills_text}
            
            ## Market Trends:
            {trends_text}
            
            ## Analysis Task:
            Provide comprehensive career development recommendations tailored to this professsional's background and market conditions.
            
            ## Response Format:
            **Career Assessment:**
            [Analysis of current career position and market value]
            
            **Growth Opportunities:**
            1. **Vertical Growth:** [Advancement within current field/role]
            2. **Lateral Moves:** [Adjacent roles that leverage existing skills]
            3. **Career Pivots:** [New directions based on transferable skills]
            
            **Skill Development Strategy:**
            - **Core Skill Enhancement:** [How to deepen existing expertise]
            - **Complementary Skills:** [Skills that would enhance current profile]
            - **Future-Proofing Skills:** [Emerging skills for long-term career security]

            **Market-Aligned Recommendations:**
            - [How to position for trending opportunities]
            - [Which market demands align with current skills]
            - [Emerging fields where skills would be valuable]

            **Action Plan:**
            - **Immediate (Next 30 days):** [Quick wins and initial steps]
            - **Short-term (3-6 months):** [Skill building and positioning activities]
            - **Long-term (6-18 months):** [Strategic career moves and major developments]
            
            **Professional Development Path:**
            1. [Specific certifications or courses to pursue]
            2. [Networking and industry engagement strategies]
            3. [Portfolio or project recommendations]
            
            **Success Metrics:**
            [How to measure progress toward career goals]
            
            Provide specific, actionable guidance that balance current market realities with long-term growth potential.
        """
        
        return prompt
    
    
    