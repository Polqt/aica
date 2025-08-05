import logging
from pydoc import text
import re
import json
from typing import List, Dict, Set
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ExtractedSkills:
    technical_skills: List[str]
    soft_skills: List[str]
    confidence_scores: Dict[str, float]
    total_skills: int
    
class SkillsExtractor:
    def __init__(self):
        self.tech_skills = self._load_tech_skills()
        self.soft_skills = self._load_soft_skills()
        self.compiled_patterns = self._compile_skill_patterns()
        
    def extract_skills_from_text(self, job_description: str) -> ExtractedSkills:
        """Main method to extract skills from job description"""
        if not job_description or not isinstance(job_description, str) or job_description.strip() == "":
            logging.debug("No job description provided for skill extraction.")
            return ExtractedSkills(
                technical_skills=[],
                soft_skills=[],
                all_skills=[],
                skill_categories={},
                confidence_scores={}
            )

        try:
            text_lower = job_description.lower()
            found_skills = {}
            skill_categories = {}
            
            # Extract technical skills
            for category, skills in self.tech_skills.items():
                category_skills = []
                for skill in skills:
                    if skill.lower() in text_lower:
                        category_skills.append(skill)
                if category_skills:
                    found_skills[category] = category_skills
                    skill_categories[category] = category_skills
            
            # Extract soft skills
            for category, skills in self.soft_skills.items():
                category_skills = []
                for skill in skills:
                    if skill.lower() in text_lower:
                        category_skills.append(skill)
                if category_skills:
                    found_skills[category] = category_skills
                    skill_categories[category] = category_skills
            
            # Compile final lists
            tech_skills = []
            soft_skills = []
            
            for category, skills in found_skills.items():
                if category in self.tech_skills:
                    tech_skills.extend(skills)
                elif category in self.soft_skills:
                    soft_skills.extend(skills)
            
            # Remove duplicates
            tech_skills = list(set(tech_skills))
            soft_skills = list(set(soft_skills))
            all_skills = tech_skills + soft_skills
            confidence_scores = {skill: 0.8 for skill in all_skills}
        
            return ExtractedSkills(
                technical_skills=tech_skills,
                soft_skills=soft_skills,
                all_skills=all_skills,
                skill_categories=skill_categories,
                confidence_scores=confidence_scores
            )
        
        except Exception as e:
            logging.error(f"Error in skills extraction: {e}")
            return ExtractedSkills(
                technical_skills=[],
                soft_skills=[],
                all_skills=[],
                skill_categories={},
                confidence_scores={}
            )

    def _load_tech_skills(self) -> Dict[str, List[str]]:
        """Load technical skills dictionary"""
        tech_skills_path = Path(__file__).parent / "tech_skills.json"
        try:
            with open(tech_skills_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "programming_languages": ["Python", "JavaScript", "Java", "PHP", "C#"],
                "frameworks": ["React", "Django", "Node.js", "Angular", "Vue.js"]
            }
    
    def _load_soft_skills(self) -> Set[str]:
        """Load soft skills dictionary"""
        soft_skills_path = Path(__file__).parent / "soft_skills.json"
        try:
            with open(soft_skills_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "communication": ["Communication", "Teamwork", "Leadership"],
                "problem_solving": ["Problem Solving", "Critical Thinking", "Analytical Skills"]
            }
    
    def _compile_skill_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for skill extraction"""
        patterns = {}
        
        for category, skills in self.tech_skills.items():
            pattern = r'\b(?:' + '|'.join(re.escape(skill) for skill in skills) + r')\b'
            patterns[f'tech_{category}'] = re.compile(pattern, re.IGNORECASE)
        
        for category, skills in self.soft_skills.items():
            pattern = r'\b(?:' + '|'.join(re.escape(skill) for skill in skills) + r')\b'
            patterns[f'soft_{category}'] = re.compile(pattern, re.IGNORECASE)
        
        return patterns

    def _clean_text(self, text: str) -> str:
        # Remove HTML tags if any
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Replace common separators with spaces
        text = re.sub(r'[/,;|&+]', ' ', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
        