import re 
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from .skills_extractor import SkillsExtractor

@dataclass
class ExtractedJobData:
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    work_type: Optional[str] = None
    employment_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    salary_period: Optional[str] = None
    experience_level: Optional[str] = None
    technical_skills: List[str] = None
    soft_skills: List[str] = None
    all_skills: List[str] = None
    skill_categories: Dict[str, List[str]] = None
    benefits: List[str] = None
    posting_date: Optional[datetime] = None
    raw_text: str = ""

class JobDetailExtractor:
    def __init__(self):
        self.skills_extractor = SkillsExtractor()
        self.location_patterns = self._compile_location_patterns()
        self.salary_patterns = self._compile_salary_patterns()
        self.work_type_patterns = self._compile_work_type_patterns()
        
    def extract_job_details(self, html: str, url: str, site_config: Dict[str, Any]) -> ExtractedJobData:
        soup = BeautifulSoup(html, 'html.parser')
        extracted_data = ExtractedJobData()
         
        extracted_data.job_title = self._extract_job_title(soup, site_config)
        extracted_data.company_name = self._extract_company_name(soup, site_config)
        
        description_text = self._extract_description_text(soup, site_config)
        extracted_data.raw_text = description_text
        
        extracted_data.location = self._extract_location(soup, site_config)
        extracted_data.country = self._extract_country(soup, site_config)
        extracted_data.work_type = self._extract_work_type(soup, site_config)
        extracted_data.employment_type = self._extract_employment_type(soup, site_config)
        extracted_data.experience_level = self._extract_experience_level(soup, site_config)
        
        salary_info = self._extract_salary_info(soup, site_config)
        extracted_data.salary_min = salary_info.get('min')
        extracted_data.salary_max = salary_info.get('max')
        extracted_data.salary_currency = salary_info.get('currency')
        extracted_data.salary_period = salary_info.get('period')
        
        if description_text:
            skills_result = self.skills_extractor.extract_skills_from_text(description_text)
            extracted_data.technical_skills = skills_result.technical_skills
            extracted_data.soft_skills = skills_result.soft_skills
            extracted_data.all_skills = skills_result.all_skills
            extracted_data.skill_categories = skills_result.skill_categories
        
        extracted_data.benefits = self._extract_benefits(soup, site_config)
        extracted_data.posting_date = self._extract_posting_date(soup, site_config)
        
        return extracted_data

    def _extract_job_title(self, soup: BeautifulSoup, site_config: Dict[str, Any]) -> Optional[str]:
        try:
            title_selector = site_config["selectors"]["job_title"]
            title_element = soup.select_one(title_selector)
            if title_element:
                return title_element.get_text(strip=True)
        except Exception as e:
            logging.warning(f"Error extracting job title: {str(e)}")
        return None
            
    def _extract_company_name(self, soup: BeautifulSoup, site_config: Dict[str, Any]) -> Optional[str]:
        try:
            company_selector = site_config["selectors"]["company_name"]
            company_element = soup.select_one(company_selector)
            if company_element:
                return company_element.get_text(strip=True)
        except Exception as e:
            logging.warning(f"Error extracting company name: {str(e)}")
            return None

    def _extract_description_text(self, soup: BeautifulSoup, site_config: Dict[str, Any]) -> str:
        try:
            description_selector = site_config["selectors"]["description"]
            description_element = soup.select_one(description_selector)
            if description_element:
                for element in description_element(["script", "style", "noscript"]):
                    element.decompose()
                
                text = description_element.get_text()
                
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split())
                return ' '.join(chunk for chunk in chunks if chunk)
        except Exception as e:
            logging.warning(f"Error extracting description selector: {str(e)}")
            return ""
        
    def _extract_location(self, soup: BeautifulSoup, text: str) -> Optional[str]: 
        location_selectors = [
            '[data_automation*="location"]',
            '.location', '.job-location',
            '[class*="location"]', '[id*="location"]',
        ]
        
        for selector in location_selectors:
            element = soup.select_one(selector)
            if element:
                location = element.get_text(strip=True)
                if location and len(location) > 2:
                    return location
        
        for pattern in self.location_patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).strip() 
            
        return None 

    def _extract_country(self, location: str) -> Optional[str]:
        if not location: 
            return None
        
        if any(keyword in location.lower() for keyword in ['philippines', 'manila', 'cebu', 'davao', 'ph']):
            return "Philippines"
        
        country_mapping = {
            'singapore': 'Singapore',
            'malaysia': 'Malaysia',
            'indonesia': 'Indonesia',
            'thailand': 'Thailand',
            'vietnam': 'Vietnam',
            'japan': 'Japan',
        }
        
        for keyword, country in country_mapping.items():
            if keyword in location.lower():
                return country
            
        return None

    def _compile_location_patterns(self) -> List[re.Pattern]:
        patterns = [
            re.compile(r'(?:location|based in|located in)[:\s]+([^,\n]+)', re.IGNORECASE),
            re.compile(r'(?:^|\n)([^,\n]+(?:city|metro|province|region))', re.IGNORECASE),
            re.compile(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)[,\s]*(?:Philippines|PH)', re.IGNORECASE)
        ]
        
        return patterns

    def _compile_salary_patterns(self) -> List[re.Pattern]:
        return [
            re.compile(r'(?:salary|compensation)[:\s]*₱?\s*(\d{1,3}(?:,\d{3})*)\s*(?:-|to)\s*₱?\s*(\d{1,3}(?:,\d{3})*)\s*(per\s+\w+)?', re.IGNORECASE),
            re.compile(r'₱\s*(\d{1,3}(?:,\d{3})*)\s*(?:-|to)\s*₱?\s*(\d{1,3}(?:,\d{3})*)', re.IGNORECASE),
            re.compile(r'(\d{1,3}(?:,\d{3})*)\s*(?:-|to)\s*(\d{1,3}(?:,\d{3})*)\s*(?:pesos?|php|₱)', re.IGNORECASE)
        ]
    
    def _compile_work_type_patterns(self) -> Dict[str, re.Pattern]:
        return {
            'remote': re.compile(r'\b(?:remote|work from home|wfh|telecommute|virtual)\b', re.IGNORECASE),
            'hybrid': re.compile(r'\b(?:hybrid|flexible|partially remote| mixed)\b', re.IGNORECASE),
            'onsite': re.compile(r'\b(?:on-?site|office|in-?office|in-person)\b', re.IGNORECASE)
        }
    
    def _extract_work_type(self, text: str) -> Optional[str]:
        for work_type, pattern in self.work_type_patterns.items():
            if pattern.search(text):
                return work_type
        return None
    
    def _extract_employment_type(self, text: str) -> Optional[str]:
        patterns = {
            'full-time': re.compile(r'\b(?:full-?time|permanent|regular)\b', re.IGNORECASE),
            'part-time': re.compile(r'\b(?:part-?time|casual|temporary)\b', re.IGNORECASE),
            'contract': re.compile(r'\b(?:contract|freelance|contractor)\b', re.IGNORECASE),
            'internship': re.compile(r'\b(?:internship|intern|trainee)\b', re.IGNORECASE),
        }
        
        for employee_type, pattern in patterns.items():
            if pattern.search(text):
                return employee_type
        return None
    
    def _extract_experience_level(self, text: str) -> Optional[str]:
        patterns = {
            'entry-level': re.compile(r'\b(?:entry.level|junior|graduate|fresh graduate|0.2 years)\b', re.IGNORECASE),
            'mid-level': re.compile(r'\b(?:mid.level|intermediate|3.5 years|mid-career|mid-level)\b', re.IGNORECASE),
            'senior-level': re.compile(r'\b(?:senior|lead|6\+ years?|5\+ years?| 8\+ years?)\b', re.IGNORECASE),
            'executive': re.compile(r'\b(?:director|manager|vp|c-level|chief|executive|head|leadership|lead)\b', re.IGNORECASE),
        }
        
        for level, pattern in patterns.items():
            if pattern.search(text):
                return level
        return None
    
    def _extract_salary_info(self, soup: BeautifulSoup, text: str) -> Dict[str, Any]:
        salary_info = {
            'min': None,
            'max': None,
            'currency': None,
            'period': None
        }
        
        salary_selectors = [
            '[data_automation*="salary"]',
            '.salary', '.compensation', '.pay',
            '[class*="salary"]', '[class*="pay"]'
        ]
        
        for selector in salary_selectors:
            element = soup.select_one(selector)
            if element:
                salary_text = element.get_text(strip=True)
                parsed = self._parse_salary_text(salary_text)
                if parsed['min'] or parsed['max']:
                    return parsed
        
        for pattern in self.salary_patterns:
            match = pattern.search(text)
            if match:
                min_salary = self._parse_salary_number(match.group(1))
                max_salary = self._parse_salary_number(match.group(2)) if len(match.groups()) > 1 else None
                
                salary_info.update({
                    'min': min_salary,
                    'max': max_salary,
                    'currency': 'PHP',
                    'period': match.group(3).strip() if len(match.groups()) > 2 else None
                })
                break
        return salary_info
    
    def _parse_salary_number(self, salary_str: str) -> Optional[int]:
        if not salary_str:
            return None
        
        cleaned = re.sub(r'[,\s]', '', salary_str)
        try:
            return int(cleaned)
        except ValueError:
            return None
        
    