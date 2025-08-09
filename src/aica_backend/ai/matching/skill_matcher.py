from typing import List, Dict, Any
from sqlalchemy.orm import Session
import logging
from ...database import models
from ..nlp import get_skill_extractor, get_similarity_calculator
from ..embeddings import get_embedding_generator, get_job_storage, get_profile_storage

logger = logging.getLogger(__name__)

class SkillMatcher:
    def __init__(self):
        self.skill_extractor = get_skill_extractor()
        self.similarity_calculator = get_similarity_calculator()
        self.embedding_generator = get_embedding_generator()
        self.job_storage = get_job_storage()
        self.profile_storage = get_profile_storage()
    
    def match_profile_skills_to_jobs(self, 
                                   db: Session,
                                   profile: models.Profile,
                                   limit: int = 50,
                                   threshold: float = 0.6) -> List[Dict[str, Any]]:
        try:
            # Extract profile skills
            profile_data = self._profile_to_dict(profile)
            profile_skills = self.skill_extractor.extract_skills_from_profile(profile_data)
            
            if not profile_skills['all']:
                logger.warning(f"No skills found for profile {profile.id}")
                return []

            profile_embedding = self.embedding_generator.generate_profile_embedding(profile_data)

            similar_jobs = self.job_storage.search_similar(
                query_embedding=profile_embedding,
                k=limit * 2,
                threshold=threshold * 0.8
            )
            
            if not similar_jobs:
                return self._fallback_skill_matching(db, profile_skills['all'], limit, threshold)

            matches = []
            job_ids = [job_id for job_id, _ in similar_jobs]
            jobs = db.query(models.JobPosting).filter(models.JobPosting.id.in_(job_ids)).all()
            
            for job in jobs:
                match_result = self._calculate_job_match_score(job, profile_skills, profile_data)
                if match_result['overall_score'] >= threshold:
                    matches.append(match_result)

            matches.sort(key=lambda x: x['overall_score'], reverse=True)
            
            return matches[:limit]
            
        except Exception as e:
            logger.error(f"Error matching profile skills to jobs: {str(e)}")
            return []
    
    def match_job_requirements_to_profiles(self,
                                         db: Session,
                                         job: models.JobPosting,
                                         limit: int = 50,
                                         threshold: float = 0.6) -> List[Dict[str, Any]]:

        try:
            # Extract job skills and requirements
            job_data = self._job_to_dict(job)
            job_skills = self.skill_extractor.extract_skills_from_job_posting(job_data)
            
            if not job_skills['all']:
                logger.warning(f"No skills found for job {job.id}")
                return []

            job_embedding = self.embedding_generator.generate_job_embedding(job_data)

            similar_profiles = self.profile_storage.search_similar(
                query_embedding=job_embedding,
                k=limit * 2,
                threshold=threshold * 0.8
            )
            
            if not similar_profiles:
                return self._fallback_profile_matching(db, job_skills['all'], limit, threshold)

            matches = []
            profile_ids = [profile_id for profile_id, _ in similar_profiles]
            profiles = db.query(models.Profile).filter(models.Profile.id.in_(profile_ids)).all()
            
            for profile in profiles:
                match_result = self._calculate_profile_match_score(profile, job_skills, job_data)
                if match_result['overall_score'] >= threshold:
                    matches.append(match_result)
            
            # Sort by overall score
            matches.sort(key=lambda x: x['overall_score'], reverse=True)
            
            return matches[:limit]
            
        except Exception as e:
            logger.error(f"Error matching job requirements to profiles: {str(e)}")
            return []
    
    def calculate_skill_gap_analysis(self,
                                   profile_skills: List[str],
                                   job_skills: List[str]) -> Dict[str, Any]:

        try:
            profile_skills_norm = {skill.lower().strip() for skill in profile_skills}
            job_skills_norm = {skill.lower().strip() for skill in job_skills}

            matching_skills = profile_skills_norm.intersection(job_skills_norm)
            missing_skills = job_skills_norm - profile_skills_norm
            extra_skills = profile_skills_norm - job_skills_norm

            total_required = len(job_skills_norm)
            matched_count = len(matching_skills)
            
            match_percentage = (matched_count / total_required * 100) if total_required > 0 else 0
            
            return {
                'match_percentage': match_percentage,
                'matching_skills': list(matching_skills),
                'missing_skills': list(missing_skills),
                'extra_skills': list(extra_skills),
                'total_required_skills': total_required,
                'matched_skills_count': matched_count,
                'missing_skills_count': len(missing_skills),
                'skill_coverage_score': match_percentage / 100
            }
            
        except Exception as e:
            logger.error(f"Error calculating skill gap analysis: {str(e)}")
            return {
                'match_percentage': 0,
                'matching_skills': [],
                'missing_skills': job_skills,
                'extra_skills': profile_skills,
                'total_required_skills': len(job_skills),
                'matched_skills_count': 0,
                'missing_skills_count': len(job_skills),
                'skill_coverage_score': 0
            }
    
    def suggest_skills_for_profile(self,
                                 db: Session,
                                 profile: models.Profile,
                                 target_jobs: List[models.JobPosting] = None,
                                 limit: int = 10) -> List[Dict[str, Any]]:

        try:
            profile_data = self._profile_to_dict(profile)
            current_skills = self.skill_extractor.extract_skills_from_profile(profile_data)
            current_skills_set = {skill.lower() for skill in current_skills['all']}

            if not target_jobs:
                matches = self.match_profile_skills_to_jobs(db, profile, limit=20, threshold=0.3)
                job_ids = [match['job_id'] for match in matches]
                target_jobs = db.query(models.JobPosting).filter(
                    models.JobPosting.id.in_(job_ids)
                ).all()
            
            # Collect skills from target jobs
            skill_frequency = {}
            skill_job_count = {}
            
            for job in target_jobs:
                job_data = self._job_to_dict(job)
                job_skills = self.skill_extractor.extract_skills_from_job_posting(job_data)
                
                for skill in job_skills['all']:
                    skill_lower = skill.lower()
                    if skill_lower not in current_skills_set:
                        skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 1
                        skill_job_count[skill_lower] = skill_job_count.get(skill_lower, 0) + 1
            
            # Calculate relevance scores
            total_jobs = len(target_jobs)
            suggestions = []
            
            for skill, frequency in skill_frequency.items():
                relevance_score = frequency / total_jobs if total_jobs > 0 else 0
                demand_score = skill_job_count[skill] / total_jobs if total_jobs > 0 else 0
                
                suggestions.append({
                    'skill_name': skill.title(),
                    'relevance_score': relevance_score,
                    'demand_score': demand_score,
                    'job_count': skill_job_count[skill],
                    'market_trend': self._determine_skill_trend(skill),
                    'category': self.skill_extractor.get_skill_category(skill) or 'other'
                })
            
            # Sort by relevance score
            suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Error suggesting skills for profile: {str(e)}")
            return []
    
    def _calculate_job_match_score(self, 
                                 job: models.JobPosting,
                                 profile_skills: Dict[str, List[str]],
                                 profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed match score between job and profile"""
        
        # Extract job skills
        job_data = self._job_to_dict(job)
        job_skills = self.skill_extractor.extract_skills_from_job_posting(job_data)
        
        # Skill matching
        skill_analysis = self.calculate_skill_gap_analysis(
            profile_skills['all'], 
            job_skills['all']
        )
        
        # Experience level matching
        experience_score = self._calculate_experience_match(profile_data, job_data)
        
        # Location matching
        location_score = self._calculate_location_match(profile_data, job_data)
        
        # Calculate overall score
        weights = {
            'skill_score': 0.6,
            'experience_score': 0.25,
            'location_score': 0.15
        }
        
        overall_score = (
            skill_analysis['skill_coverage_score'] * weights['skill_score'] +
            experience_score * weights['experience_score'] +
            location_score * weights['location_score']
        )
        
        return {
            'job_id': job.id,
            'job_title': job.job_title,
            'company_name': job.company_name,
            'overall_score': overall_score,
            'skill_analysis': skill_analysis,
            'experience_score': experience_score,
            'location_score': location_score,
            'match_reasons': self._generate_match_reasons(skill_analysis, experience_score, location_score),
            'improvement_suggestions': self._generate_improvement_suggestions(skill_analysis)
        }
    
    def _calculate_profile_match_score(self,
                                     profile: models.Profile,
                                     job_skills: Dict[str, List[str]],
                                     job_data: Dict[str, Any]) -> Dict[str, Any]:

        profile_data = self._profile_to_dict(profile)
        profile_skills = self.skill_extractor.extract_skills_from_profile(profile_data)

        skill_analysis = self.calculate_skill_gap_analysis(
            profile_skills['all'],
            job_skills['all']
        )
        
        experience_score = self._calculate_experience_match(profile_data, job_data)
        location_score = self._calculate_location_match(profile_data, job_data)
        
        weights = {
            'skill_score': 0.6,
            'experience_score': 0.25,
            'location_score': 0.15
        }
        
        overall_score = (
            skill_analysis['skill_coverage_score'] * weights['skill_score'] +
            experience_score * weights['experience_score'] +
            location_score * weights['location_score']
        )
        
        return {
            'profile_id': profile.id,
            'user_name': f"{profile.first_name} {profile.last_name}",
            'professional_title': profile.professional_title,
            'overall_score': overall_score,
            'skill_analysis': skill_analysis,
            'experience_score': experience_score,
            'location_score': location_score
        }
    
    def _profile_to_dict(self, profile: models.Profile) -> Dict[str, Any]:
        return {
            'professional_title': profile.professional_title,
            'summary': profile.summary,
            'skills': [{'name': skill.name} for skill in profile.skills] if profile.skills else [],
            'experiences': [
                {
                    'job_title': exp.job_title,
                    'company_name': exp.company_name,
                    'description': exp.description
                }
                for exp in profile.experiences
            ] if profile.experiences else [],
            'educations': [
                {
                    'degree': edu.degree,
                    'field_of_study': edu.field_of_study,
                    'institution_name': edu.institution_name,
                    'description': edu.description
                }
                for edu in profile.educations
            ] if profile.educations else []
        }
    
    def _job_to_dict(self, job: models.JobPosting) -> Dict[str, Any]:
        return {
            'job_title': job.job_title,
            'company_name': job.company_name,
            'full_text': job.full_text,
            'location': job.location,
            'work_type': job.work_type,
            'employment_type': job.employment_type,
            'experience_level': job.experience_level,
            'all_skills': job.all_skills or [],
            'technical_skills': job.technical_skills or [],
            'soft_skills': job.soft_skills or [],
            'requirements': job.requirements or []
        }
    
    def _calculate_experience_match(self, profile_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        job_level = job_data.get('experience_level', '').lower()

        experience_count = len(profile_data.get('experiences', []))
        
        if job_level == 'entry' and experience_count <= 2:
            return 1.0
        elif job_level == 'mid' and 2 <= experience_count <= 5:
            return 1.0
        elif job_level == 'senior' and experience_count >= 5:
            return 1.0
        else:
            return 0.7
    
    def _calculate_location_match(self, profile_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        job_work_type = job_data.get('work_type', '').lower()
        
        if 'remote' in job_work_type:
            return 1.0

        return 0.8
    
    def _generate_match_reasons(self, skill_analysis: Dict[str, Any], 
                              experience_score: float, location_score: float) -> List[str]:
        reasons = []
        
        if skill_analysis['match_percentage'] >= 70:
            reasons.append(f"Strong skill match ({skill_analysis['match_percentage']:.1f}%)")
        elif skill_analysis['match_percentage'] >= 50:
            reasons.append(f"Good skill match ({skill_analysis['match_percentage']:.1f}%)")
        
        if experience_score >= 0.8:
            reasons.append("Experience level matches well")
        
        if location_score >= 0.8:
            reasons.append("Location compatibility")
        
        if skill_analysis['matching_skills']:
            key_skills = skill_analysis['matching_skills'][:3]
            reasons.append(f"Key matching skills: {', '.join(key_skills)}")
        
        return reasons
    
    def _generate_improvement_suggestions(self, skill_analysis: Dict[str, Any]) -> List[str]:
        suggestions = []
        
        if skill_analysis['missing_skills']:
            missing_count = len(skill_analysis['missing_skills'])
            if missing_count <= 3:
                skills_text = ', '.join(skill_analysis['missing_skills'][:3])
                suggestions.append(f"Consider learning: {skills_text}")
            else:
                suggestions.append(f"Consider learning {missing_count} additional skills")
        
        if skill_analysis['match_percentage'] < 50:
            suggestions.append("Focus on developing core technical skills for this role")
        
        return suggestions

    
    def _fallback_skill_matching(self, db: Session, skills: List[str], limit: int, threshold: float) -> List[Dict[str, Any]]:
        skill_lower = [skill.lower() for skill in skills]
        
        jobs = db.query(models.JobPosting).filter(
            models.JobPosting.status == 'processed'
        ).limit(limit * 2).all()
        
        matches = []
        for job in jobs:
            if job.all_skills:
                job_skills_lower = [skill.lower() for skill in job.all_skills]
                overlap = len(set(skill_lower).intersection(set(job_skills_lower)))
                score = overlap / len(set(skill_lower + job_skills_lower)) if (skill_lower + job_skills_lower) else 0
                
                if score >= threshold:
                    matches.append({
                        'job_id': job.id,
                        'job_title': job.job_title,
                        'company_name': job.company_name,
                        'overall_score': score,
                        'skill_analysis': {
                            'match_percentage': score * 100,
                            'matching_skills': list(set(skill_lower).intersection(set(job_skills_lower))),
                            'skill_coverage_score': score
                        }
                    })
        
        matches.sort(key=lambda x: x['overall_score'], reverse=True)
        return matches[:limit]

    def _fallback_profile_matching(self, db: Session, skills: List[str], limit: int, threshold: float) -> List[Dict[str, Any]]:
        profiles = db.query(models.Profile).limit(limit * 2).all()

        matches = []
        for profile in profiles:
            profile_skills = [skill.name.lower() for skill in profile.skills] if profile.skills else []
            skill_lower = [skill.lower() for skill in skills]

            overlap = len(set(skill_lower).intersection(set(profile_skills)))
            score = overlap / len(set(skill_lower + profile_skills)) if (skill_lower + profile_skills) else 0

            if score >= threshold:
                matches.append({
                    'profile_id': profile.id,
                    'user_name': f"{profile.first_name} {profile.last_name}",
                    'professional_title': profile.professional_title,
                    'overall_score': score
                })

        matches.sort(key=lambda x: x['overall_score'], reverse=True)
        return matches[:limit]


# Global skill matcher instance
_skill_matcher = None

def get_skill_matcher() -> SkillMatcher:
    global _skill_matcher
    if _skill_matcher is None:
        _skill_matcher = SkillMatcher()
    return _skill_matcher
