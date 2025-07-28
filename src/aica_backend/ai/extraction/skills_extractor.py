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
        
    def extract_skills(self, job_description: str) -> ExtractedSkills:
        """Main method to extract skills from job description"""
        pass

    def _load_tech_skills(self) -> Set[str]:
        """Load technical skills dictionary"""
        tech_skills_path = Path(__file__).parent / "tech_skills.json"
        pass
    
    def _load_soft_skills(self) -> Set[str]:
        """Load soft skills dictionary"""
        soft_skills_path = Path(__file__).parent / "soft_skills.json"
        pass
