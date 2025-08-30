"""
Prompt templates for LLM service operations.
"""

from typing import List, Dict, Any


class PromptTemplates:
    """Collection of prompt templates for various LLM operations."""

    def create_job_match_prompt(
        self,
        user_skills: List[str],
        job_title: str,
        company_name: str,
        required_skills: List[str],
        preferred_skills: List[str],
        job_description: str,
        similarity_score: float
    ) -> str:
        """Create a prompt for explaining job match compatibility."""
        return f"""
        Analyze the compatibility between a user's skills and a job posting.

        User Skills: {', '.join(user_skills)}
        Job Title: {job_title}
        Company: {company_name}
        Required Skills: {', '.join(required_skills) if required_skills else 'Not specified'}
        Preferred Skills: {', '.join(preferred_skills) if preferred_skills else 'Not specified'}
        Job Description: {job_description[:1000]}...
        Similarity Score: {similarity_score:.2%}

        Please provide a detailed analysis including:
        1. Overall match assessment
        2. Key matching skills
        3. Skill gaps that should be addressed
        4. Specific recommendations for the candidate
        5. Career development suggestions

        Be specific and actionable in your recommendations.
        """

    def create_multiple_matches_prompt(
        self,
        user_skills: List[str],
        matched_jobs: List[Dict[str, Any]]
    ) -> str:
        """Create a prompt for summarizing multiple job matches."""
        jobs_summary = "\n".join([
            f"- {job.get('title', 'Unknown')} at {job.get('company_name', 'Unknown Company')} "
            f"(Match: {job.get('similarity_score', 0):.1%})"
            for job in matched_jobs[:5]
        ])

        return f"""
        Based on the user's skills: {', '.join(user_skills)}

        Here are the top job matches found:

        {jobs_summary}

        Please provide:
        1. Overall career insights and patterns
        2. Skill priorities for development
        3. Potential career paths
        4. Next steps for the user
        5. Industry trends or opportunities

        Focus on actionable advice and long-term career development.
        """


# Create singleton instance
prompt_templates = PromptTemplates()