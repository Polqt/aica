import re
import spacy
from typing import List, Dict, Any, Optional
import logging
from collections import Counter

logger = logging.getLogger(__name__)

class SkillExtractor:
    def __init__(self):
        self.nlp = None
        self.technical_skills = set()
        self.soft_skills = set()
        self.skill_patterns = {}
        self._load_nlp_model()
        self._load_skill_databases()
    
    def _load_nlp_model(self):
        """Load spaCy NLP model"""
        try:
            # Try to load English model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy English model")
        except OSError:
            logger.warning("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
            # Fallback to basic processing
            self.nlp = None
    
    def _load_skill_databases(self):
        """Load skill databases from local files"""
        try:
            technical_skills_data = [
                # Programming Languages
                "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust", "Kotlin",
                "Swift", "TypeScript", "R", "MATLAB", "Scala", "Perl", "HTML", "CSS", "SQL",
                
                # Frameworks and Libraries
                "React", "Vue.js", "Angular", "Node.js", "Express.js", "Django", "Flask", "FastAPI",
                "Spring", "Laravel", "Ruby on Rails", "ASP.NET", "Bootstrap", "Tailwind CSS",
                "jQuery", "NumPy", "Pandas", "TensorFlow", "PyTorch", "Scikit-learn", "Keras",
                
                # Databases
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", "SQL Server",
                "Elasticsearch", "Cassandra", "DynamoDB", "Firebase",
                
                # Cloud and DevOps
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git", "GitHub",
                "GitLab", "CI/CD", "DevOps", "Linux", "Ubuntu", "CentOS", "Apache", "Nginx",
                
                # Data Science and AI
                "Machine Learning", "Deep Learning", "Data Science", "Artificial Intelligence",
                "NLP", "Computer Vision", "Statistics", "Data Analysis", "Big Data", "Hadoop",
                "Spark", "Tableau", "Power BI", "ETL", "Data Warehousing",
                
                # Mobile Development
                "iOS Development", "Android Development", "React Native", "Flutter", "Xamarin",
                
                # Other Technologies
                "REST API", "GraphQL", "Microservices", "Blockchain", "IoT", "Cybersecurity",
                "Network Security", "Penetration Testing", "OWASP", "SSL/TLS"
            ]
            
            # Soft skills database
            soft_skills_data = [
                "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking",
                "Time Management", "Project Management", "Analytical Thinking", "Creativity",
                "Adaptability", "Collaboration", "Decision Making", "Attention to Detail",
                "Organization", "Multitasking", "Initiative", "Self-motivated", "Proactive",
                "Customer Service", "Presentation Skills", "Public Speaking", "Writing",
                "Research", "Planning", "Coordination", "Mentoring", "Training", "Coaching",
                "Conflict Resolution", "Negotiation", "Empathy", "Emotional Intelligence",
                "Stress Management", "Work-Life Balance", "Professional Development"
            ]
            
            # Convert to sets for faster lookup
            self.technical_skills = {skill.lower() for skill in technical_skills_data}
            self.soft_skills = {skill.lower() for skill in soft_skills_data}
            
            # Create pattern mapping for better matching
            self._create_skill_patterns()
            
            logger.info(f"Loaded {len(self.technical_skills)} technical skills and {len(self.soft_skills)} soft skills")
            
        except Exception as e:
            logger.error(f"Failed to load skill databases: {str(e)}")
    
    def _create_skill_patterns(self):
        self.skill_patterns = {}
        
        # Combine all skills
        all_skills = list(self.technical_skills) + list(self.soft_skills)
        
        for skill in all_skills:
            # Create flexible patterns for skill matching
            # Handle variations like "Python programming", "JavaScript developer", etc.
            escaped_skill = re.escape(skill)
            patterns = [
                rf'\b{escaped_skill}\b',  # Exact match
                rf'\b{escaped_skill}(?:ing|er|ed|s)?\b',  # With common suffixes
                rf'\b(?:experience\s+(?:with|in)\s+)?{escaped_skill}\b',  # "experience with X"
                rf'\b{escaped_skill}(?:\s+(?:programming|development|developer|engineer|engineering|skills?|experience))?\b'
            ]
            
            self.skill_patterns[skill] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def extract_skills_from_text(self, text: str) -> Dict[str, List[str]]:
        if not text:
            return {"technical": [], "soft": [], "all": []}
        
        # Clean text
        cleaned_text = self._clean_text(text)
        
        # Extract using different methods
        technical_skills = self._extract_technical_skills(cleaned_text)
        soft_skills = self._extract_soft_skills(cleaned_text)
        
        # Combine and deduplicate
        all_skills = list(set(technical_skills + soft_skills))
        
        return {
            "technical": technical_skills,
            "soft": soft_skills,
            "all": all_skills
        }
    
    def extract_skills_from_job_posting(self, job_data: Dict[str, Any]) -> Dict[str, List[str]]:
        # Combine relevant text fields
        text_parts = []
        
        if job_data.get('job_title'):
            text_parts.append(job_data['job_title'])
        
        if job_data.get('full_text'):
            text_parts.append(job_data['full_text'])
        
        # Look for requirements section specifically
        if job_data.get('requirements'):
            if isinstance(job_data['requirements'], list):
                text_parts.extend(job_data['requirements'])
            else:
                text_parts.append(str(job_data['requirements']))
        
        combined_text = " ".join(text_parts)
        
        # Extract skills
        skills = self.extract_skills_from_text(combined_text)
        
        # Add job-specific skill extraction logic
        skills = self._enhance_job_skills(skills, job_data)
        
        return skills
    
    def extract_skills_from_profile(self, profile_data: Dict[str, Any]) -> Dict[str, List[str]]:
        text_parts = []
        
        # Professional title
        if profile_data.get('professional_title'):
            text_parts.append(profile_data['professional_title'])
        
        # Summary
        if profile_data.get('summary'):
            text_parts.append(profile_data['summary'])
        
        # Experience descriptions
        if profile_data.get('experiences'):
            for exp in profile_data['experiences']:
                if exp.get('job_title'):
                    text_parts.append(exp['job_title'])
                if exp.get('description'):
                    if isinstance(exp['description'], list):
                        text_parts.extend(exp['description'])
                    else:
                        text_parts.append(str(exp['description']))
        
        # Education
        if profile_data.get('educations'):
            for edu in profile_data['educations']:
                if edu.get('field_of_study'):
                    text_parts.append(edu['field_of_study'])
                if edu.get('description'):
                    text_parts.append(edu['description'])
        
        combined_text = " ".join(text_parts)
        
        # Extract skills
        skills = self.extract_skills_from_text(combined_text)
        
        # Add explicitly listed skills if available
        if profile_data.get('skills'):
            explicit_skills = [skill.get('name', '') for skill in profile_data['skills']]
            skills = self._merge_skill_lists(skills, explicit_skills)
        
        return skills
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        found_skills = set()
        
        for skill in self.technical_skills:
            for pattern in self.skill_patterns.get(skill, []):
                if pattern.search(text):
                    found_skills.add(skill.title())  # Normalize case
                    break
        
        return list(found_skills)
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        found_skills = set()
        
        for skill in self.soft_skills:
            for pattern in self.skill_patterns.get(skill, []):
                if pattern.search(text):
                    found_skills.add(skill.title())  # Normalize case
                    break
        
        return list(found_skills)
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common formatting artifacts
        cleaned = re.sub(r'[•\-\*]\s*', ' ', cleaned)  # Remove bullet points
        cleaned = re.sub(r'\n+', ' ', cleaned)  # Replace newlines with spaces
        
        return cleaned
    
    def _enhance_job_skills(self, skills: Dict[str, List[str]], job_data: Dict[str, Any]) -> Dict[str, List[str]]:
        # Infer skills from job title
        job_title = job_data.get('job_title', '').lower()
        
        # Add common skills based on job title patterns
        title_skill_mapping = {
            'python': ['Python', 'Django', 'Flask'],
            'javascript': ['JavaScript', 'Node.js', 'React'],
            'data scientist': ['Python', 'R', 'Machine Learning', 'Statistics'],
            'devops': ['Docker', 'Kubernetes', 'AWS', 'CI/CD'],
            'frontend': ['HTML', 'CSS', 'JavaScript', 'React'],
            'backend': ['Python', 'Java', 'SQL', 'REST API'],
            'full stack': ['JavaScript', 'Python', 'SQL', 'HTML', 'CSS']
        }
        
        for pattern, implied_skills in title_skill_mapping.items():
            if pattern in job_title:
                for skill in implied_skills:
                    if skill.lower() in self.technical_skills and skill not in skills['technical']:
                        skills['technical'].append(skill)
                        if skill not in skills['all']:
                            skills['all'].append(skill)
        
        return skills
    
    def _merge_skill_lists(self, extracted_skills: Dict[str, List[str]], explicit_skills: List[str]) -> Dict[str, List[str]]:
        # Categorize explicit skills
        for skill in explicit_skills:
            skill_lower = skill.lower()
            skill_title = skill.title()
            
            if skill_lower in self.technical_skills:
                if skill_title not in extracted_skills['technical']:
                    extracted_skills['technical'].append(skill_title)
            elif skill_lower in self.soft_skills:
                if skill_title not in extracted_skills['soft']:
                    extracted_skills['soft'].append(skill_title)
            
            # Add to all skills if not already present
            if skill_title not in extracted_skills['all']:
                extracted_skills['all'].append(skill_title)
        
        return extracted_skills
    
    def get_skill_category(self, skill: str) -> Optional[str]:
        """Get the category of a skill"""
        skill_lower = skill.lower()
        
        if skill_lower in self.technical_skills:
            return "technical"
        elif skill_lower in self.soft_skills:
            return "soft"
        else:
            return None
    
    def calculate_skill_frequency(self, texts: List[str]) -> Dict[str, int]:
        """Calculate skill frequency across multiple texts"""
        skill_counter = Counter()
        
        for text in texts:
            skills = self.extract_skills_from_text(text)
            for skill in skills['all']:
                skill_counter[skill] += 1
        
        return dict(skill_counter)

_skill_extractor = None

def get_skill_extractor() -> SkillExtractor:
    global _skill_extractor
    if _skill_extractor is None:
        _skill_extractor = SkillExtractor()
    return _skill_extractor
