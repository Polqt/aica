import re
from typing import Optional, List

def clean_text(text: Optional[str]) -> str:
    if not text or not isinstance(text, str):
        return ''
    return re.sub(r'\s+', ' ', text).strip()

def normalize_employment_type(employment_type: Optional[str]) -> str:
    if not employment_type:
        return ''
    et_lower = employment_type.lower()
    if 'full-time' in et_lower or 'full time' in et_lower:
        return 'full-time'
    if 'part-time' in et_lower or 'part time' in et_lower:
        return 'part-time'
    if 'contract' in et_lower:
        return 'contract'
    if 'intern' in et_lower:
        return 'internship'
    return clean_text(employment_type)

def normalize_experience_level(experience: Optional[str]) -> str:
    if not experience:
        return ''
    exp_lower = experience.lower()
    if any(word in exp_lower for word in ['entry', 'junior', 'fresh']):
        return 'entry'
    if any(word in exp_lower for word in ['senior', 'lead', 'principal']):
        return 'senior'
    if any(word in exp_lower for word in ['mid', 'intermediate']):
        return 'mid-level'
    return clean_text(experience)

def clean_date(date_str: Optional[str]) -> str:
    return clean_text(date_str)

def categorize_tech_job(title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    if any(word in text for word in ['data', 'analyst', 'scientist', 'ml', 'ai']):
        return 'Data & AI'
    if any(word in text for word in ['devops', 'cloud', 'sre']):
        return 'DevOps & Cloud'
    if any(word in text for word in ['security', 'cyber']):
        return 'Cybersecurity'
    if any(word in text for word in ['mobile', 'android', 'ios']):
        return 'Mobile Development'
    if any(word in text for word in ['frontend', 'front-end', 'ui', 'ux']):
        return 'Frontend Development'
    if any(word in text for word in ['backend', 'back-end', 'api']):
        return 'Backend Development'
    if any(word in text for word in ['fullstack', 'full-stack']):
        return 'Full Stack Development'
    return 'General Software Development'

def clean_skills_array(skills: Optional[List[str]]) -> List[str]:
    if not isinstance(skills, list):
        return []
    
    cleaned_skills = []
    for skill in skills:
        if isinstance(skill, str) and skill.strip():
            cleaned_skill = clean_text(skill)
            if cleaned_skill and len(cleaned_skill) < 50:
                cleaned_skills.append(cleaned_skill)
    return cleaned_skills[:15]