from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class MatchResult:
    job_id: int
    match_score: float
    compatibility_score: float
    skill_match_percentage: float
    experience_match: bool
    location_match: bool
    explanation: str
    skill_gaps: List[str]
    recommendations: List[str]
    rag_insights: Optional[str] = None

class MatchingService:
    def __init__(self, rag_service=None):
        self.rag_service = rag_service
        
        # Configurable weights 
        self.weights = {
            "skills": 0.4,
            "experience": 0.3,
            "location": 0.1,
            "work_type": 0.1,
            "salary": 0.1
        }
    
    def find_matches(self, user_profile: Dict[str, Any], jobs: List[Dict[str, Any]], 
                    top_k: int = 10) -> List[MatchResult]:
        try:
            matches = []
            
            for job in jobs:
                match_result = self._calculate_match(user_profile, job)
                if match_result.match_score > 0.2:  # Minimum threshold
                    matches.append(match_result)
            
            # Sort by match score (descending)
            matches.sort(key=lambda x: x.match_score, reverse=True)
            
            return matches[:top_k]
            
        except Exception as e:
            logger.error(f"Failed to find matches: {str(e)}")
            return []
    
    def _calculate_match(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> MatchResult:
        scores = {}
        
        # Calculate individual scores
        scores["skills"] = self._calculate_skill_match(user_profile, job)
        scores["experience"] = self._calculate_experience_match(user_profile, job)
        scores["location"] = self._calculate_location_match(user_profile, job)
        scores["work_type"] = self._calculate_work_type_match(user_profile, job)
        scores["salary"] = self._calculate_salary_match(user_profile, job)
        
        # Calculate weighted overall score
        overall_score = sum(scores[key] * self.weights[key] for key in scores)
        
        # Generate explanation and recommendations
        explanation = self._generate_basic_explanation(scores, job)
        skill_gaps = self._identify_skill_gaps(user_profile, job)
        recommendations = self._generate_recommendations(scores, skill_gaps)
        
        # Get RAG insights if available
        rag_insights = None
        if self.rag_service:
            try:
                rag_insights = self.rag_service.explain_job_match(job, user_profile)
            except Exception as e:
                logger.warning(f"RAG insights failed: {str(e)}")
        
        return MatchResult(
            job_id=job.get("id", 0),
            match_score=overall_score,
            compatibility_score=overall_score,  # Same for now (YAGNI)
            skill_match_percentage=scores["skills"] * 100,
            experience_match=scores["experience"] > 0.7,
            location_match=scores["location"] > 0.8,
            explanation=explanation,
            skill_gaps=skill_gaps,
            recommendations=recommendations,
            rag_insights=rag_insights
        )
    
    def _calculate_skill_match(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> float:
        user_skills = self._extract_user_skills(user_profile)
        job_text = job.get("full_text", "").lower()
        
        if not user_skills or not job_text:
            return 0.0
        
        # Simple keyword matching (RAG provides contextual understanding)
        matches = 0
        total_skills = len(user_skills)
        
        for skill in user_skills:
            if skill.lower() in job_text:
                matches += 1
        
        return matches / total_skills if total_skills > 0 else 0.0
    
    def _calculate_experience_match(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> float:
        """Calculate experience level matching"""
        user_years = self._calculate_total_experience(user_profile)
        job_level = job.get("experience_level", "").lower()

        level_requirements = {
            "entry": (0, 2),
            "junior": (1, 3),
            "mid": (3, 6),
            "senior": (5, 10),
            "lead": (7, 15),
            "executive": (10, 20)
        }
        
        for level, (min_years, max_years) in level_requirements.items():
            if level in job_level:
                if min_years <= user_years <= max_years:
                    return 1.0
                elif user_years < min_years:
                    return max(0.0, 1.0 - (min_years - user_years) * 0.2)
                else:
                    return max(0.0, 1.0 - (user_years - max_years) * 0.1)
        
        return 0.5  # Neutral if can't determine
    
    def _calculate_location_match(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> float:
        user_location = user_profile.get("location", "").lower()
        job_location = job.get("location", "").lower()
        work_type = job.get("work_type", "").lower()
        
        # Remote work gets high score
        if "remote" in work_type or "hybrid" in work_type:
            return 0.9
        
        # Simple location matching
        if user_location and job_location:
            if user_location in job_location or job_location in user_location:
                return 1.0
            else:
                return 0.3  # Different location but still possible
        
        return 0.5  # Neutral if location not specified
    
    def _calculate_work_type_match(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> float:
        """Calculate work type preference match"""
        user_prefs = user_profile.get("work_preferences", {})
        preferred_types = user_prefs.get("work_types", [])
        job_work_type = job.get("work_type", "").lower()
        
        if not preferred_types:
            return 0.5  # Neutral if no preference
        
        # Check if job work type matches user preferences
        for pref in preferred_types:
            if pref.lower() in job_work_type:
                return 1.0
        
        return 0.3  # Lower score for non-preferred work type
    
    def _calculate_salary_match(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> float:
        """Calculate salary expectation match"""
        user_prefs = user_profile.get("work_preferences", {})
        min_expected = user_prefs.get("minimum_salary")
        
        job_min = job.get("salary_min")
        job_max = job.get("salary_max")
        
        if not min_expected or not job_min:
            return 0.5  # Neutral if salary not specified
        
        # Check if job salary meets expectations
        if job_max and job_max >= min_expected:
            return 1.0
        elif job_min >= min_expected * 0.8:  # Within 20% of expectation
            return 0.8
        else:
            return 0.2  # Below expectations
    
    def _extract_user_skills(self, user_profile: Dict[str, Any]) -> List[str]:
        """Extract skill names from user profile"""
        skills = user_profile.get("skills", [])
        
        if not skills:
            return []
        
        skill_names = []
        for skill in skills:
            if isinstance(skill, dict):
                skill_names.append(skill.get("name", ""))
            else:
                skill_names.append(str(skill))
        
        return [s for s in skill_names if s]  # Remove empty strings
    
    def _calculate_total_experience(self, user_profile: Dict[str, Any]) -> float:
        """Calculate total years of experience"""
        experiences = user_profile.get("experiences", [])
        
        if not experiences:
            return 0.0
        
        total_months = 0
        for exp in experiences:
            start_date = exp.get("start_date")
            end_date = exp.get("end_date") or datetime.now().date()
            
            if start_date:
                if isinstance(start_date, str):
                    try:
                        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                    except:
                        continue
                
                if isinstance(end_date, str):
                    try:
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                    except:
                        end_date = datetime.now().date()
                
                duration = end_date - start_date
                total_months += duration.days / 30.44  # Average days per month
        
        return total_months / 12  # Convert to years
    
    def _generate_basic_explanation(self, scores: Dict[str, float], job: Dict[str, Any]) -> str:
        """Generate human-readable explanation"""
        explanations = []
        
        if scores["skills"] > 0.7:
            explanations.append("Strong skill alignment")
        elif scores["skills"] > 0.4:
            explanations.append("Good skill match with some gaps")
        else:
            explanations.append("Limited skill overlap")
        
        if scores["experience"] > 0.8:
            explanations.append("excellent experience fit")
        elif scores["experience"] > 0.5:
            explanations.append("suitable experience level")
        else:
            explanations.append("experience level mismatch")
        
        if scores["location"] > 0.8:
            explanations.append("great location compatibility")
        
        job_title = job.get("job_title", "this position")
        return f"This {job_title} shows {', '.join(explanations)}."
    
    def _identify_skill_gaps(self, user_profile: Dict[str, Any], job: Dict[str, Any]) -> List[str]:
        """Identify missing skills (basic implementation)"""
        # This is where RAG shines - understanding skills from context
        # For now, simple keyword extraction
        user_skills = [s.lower() for s in self._extract_user_skills(user_profile)]
        job_text = job.get("full_text", "").lower()
        
        # Common tech skills to look for
        common_skills = [
            "python", "javascript", "react", "node.js", "sql", "mongodb",
            "aws", "docker", "kubernetes", "git", "agile", "scrum",
            "machine learning", "data analysis", "api", "rest"
        ]
        
        gaps = []
        for skill in common_skills:
            if skill in job_text and skill not in user_skills:
                gaps.append(skill.title())
        
        return gaps[:5]  # Limit to top 5
    
    def _generate_recommendations(self, scores: Dict[str, float], skill_gaps: List[str]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if scores["skills"] < 0.5:
            recommendations.append("Consider developing relevant technical skills")
        
        if skill_gaps:
            recommendations.append(f"Focus on learning: {', '.join(skill_gaps[:3])}")
        
        if scores["experience"] < 0.4:
            recommendations.append("Gain more experience in this field")
        
        if scores["salary"] < 0.5:
            recommendations.append("Salary expectations may need adjustment")
        
        return recommendations

_matching_service = None

def get_matching_service(rag_service=None):
    global _matching_service
    if _matching_service is None:
        _matching_service = MatchingService(rag_service)
    return _matching_service
