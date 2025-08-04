import re 
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from bs4 import BeautifulSoup
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
    external_id: Optional[str] = None
    extraction_quality_score: float = 0.0
    raw_text: str = ""

class JobDetailExtractor:
    def __init__(self):
        self.skills_extractor = SkillsExtractor()
        self.location_patterns = self._compile_location_patterns()
        self.salary_patterns = self._compile_salary_patterns()
        self.work_type_patterns = self._compile_work_type_patterns()
        
    def extract_job_details(self, html: str, url: str, site_config: Dict[str, Any]) -> ExtractedJobData:
        try:
            if not html or html.strip() == "":
                logging.warning(f"No HTML content to extract from {url}")
                return self._create_empty_extracted_data()
            
            soup = BeautifulSoup(html, 'html.parser')
            extracted_data = ExtractedJobData()
            
            extracted_data.job_title = self._extract_job_title(soup, site_config)
            extracted_data.company_name = self._extract_company_name(soup, site_config)
            extracted_data.external_id = self._extract_external_id(url)
            
            description_text = self._extract_description_text(soup, site_config)
            extracted_data.raw_text = description_text or ""
            
            extracted_data.location = self._extract_location(soup, site_config)
            extracted_data.country = self._extract_country(extracted_data.location)
            extracted_data.work_type = self._extract_work_type(description_text or "")
            extracted_data.employment_type = self._extract_employment_type(description_text or "")
            extracted_data.experience_level = self._extract_experience_level(description_text or "")
            
            salary_info = self._extract_salary_info(soup, description_text or "") 
            extracted_data.salary_min = salary_info.get('min' or "")
            extracted_data.salary_max = salary_info.get('max' or "")
            extracted_data.salary_currency = salary_info.get('currency' or "")
            extracted_data.salary_period = salary_info.get('period' or "")
            
            if description_text and description_text.strip():
                try:
                    skills_result = self.skills_extractor.extract_skills_from_text(description_text)
                    extracted_data.technical_skills = skills_result.technical_skills
                    extracted_data.soft_skills = skills_result.soft_skills
                    extracted_data.all_skills = skills_result.all_skills
                    extracted_data.skill_categories = skills_result.skill_categories
                except Exception as e:
                    logging.warning(f"Error extracting skills: {str(e)}")
                    extracted_data.technical_skills = []
                    extracted_data.soft_skills = []
                    extracted_data.all_skills = []
                    extracted_data.skill_categories = {}
            else:
                logging.warning("No description text available for skills extraction")
                extracted_data.technical_skills = []
                extracted_data.soft_skills = []
                extracted_data.all_skills = []
                extracted_data.skill_categories = {}
            
            extracted_data.benefits = self._extract_benefits(description_text or "")
            extracted_data.posting_date = self._extract_posting_date(soup)
            
            extracted_data.extraction_quality_score = self._calculate_quality_score(extracted_data)
            return extracted_data
        except Exception as e:
            logging.error(f"Error extracting job details from {url}: {str(e)}")
            return self._create_empty_extracted_data()
    
    def _create_empty_extracted_data(self) -> ExtractedJobData:
        return ExtractedJobData(
            technical_skills=[],
            soft_skills=[],
            all_skills=[],
            skill_categories={},
            benefits=[],
            raw_text="",
            extraction_quality_score=0.0
        )

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
            company_selector = site_config["selectors"]["company"]
            company_element = soup.select_one(company_selector)
            if company_element:
                return company_element.get_text(strip=True)
        except Exception as e:
            logging.warning(f"Error extracting company name: {str(e)}")
            return None

    def _extract_description_text(self, soup: BeautifulSoup, site_config: Dict[str, Any]) -> str:
        try:
            # Try primary selector from config
            desc_selector = site_config["selectors"]["description"]
            
            # Split multiple selectors and try each one
            selectors = [s.strip() for s in desc_selector.split(',')]
            
            for selector in selectors:
                desc_element = soup.select_one(selector)
                if desc_element:
                    # Remove unwanted elements
                    for element in desc_element(["script", "style", "noscript", "svg"]):
                        element.decompose()
                    
                    text = desc_element.get_text()
                    # Clean and normalize text
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split())
                    cleaned_text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    if cleaned_text and len(cleaned_text) > 50:  # Ensure we have substantial content
                        return cleaned_text
            
            # Additional fallback selectors if config selectors fail
            fallback_selectors = [
                "div[class*='job-ad-details']",
                "div[class*='job-description']",
                "div[class*='description']",
                ".job-details",
                ".job-content",
                "main div[class*='content']"
            ]
            
            for selector in fallback_selectors:
                desc_element = soup.select_one(selector)
                if desc_element:
                    text = desc_element.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split())
                    cleaned_text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    if cleaned_text and len(cleaned_text) > 50:
                        logging.info(f"Used fallback selector: {selector}")
                        return cleaned_text
            
            logging.warning("No description content found with any selector")
            return ""
            
        except Exception as e:
            logging.warning(f"Error extracting description: {e}")
            return ""
        
    def _extract_external_id(self, url: str) -> Optional[str]:
        match = re.search(r'/job/(\d+)', url)
        return match.group(1) if match else None
        
    def _extract_location(self, soup: BeautifulSoup, site_config: Dict[str, Any]) -> Optional[str]: 
        try:
            
            if "location" in site_config.get("selectors", {}):
                location_selectors = site_config["selectors"]["location"]
                location_element = soup.select_one(location_selectors)
                if location_element:
                    location_text = location_element.get_text(strip=True)
                    if location_text and len(location_text) > 2:
                        return location_text
            
            location_selectors = [
                '[data-automation*="location"]',
                '.location', '.job-location',
                '[class*="location"]', '[id*="location"]',
            ]
            
            for selector in location_selectors:
                element = soup.select_one(selector)
                if element:
                    location = element.get_text(strip=True)
                    if location and len(location) > 2:
                        return location
            return None 
        except Exception as e:
            logging.warning(f"Error extracting location: {str(e)}")
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
        """Extract work type with enhanced patterns"""
        if not text or not isinstance(text, str):
            return None
            
        text_lower = text.lower()
        
        # Enhanced patterns based on your job titles
        patterns = {
            'remote': r'\b(?:remote|work from home|wfh|telecommute|work remotely)\b',
            'hybrid': r'\b(?:hybrid|flexible|mixed|partially remote)\b',
            'onsite': r'\b(?:on-?site|office|in-person|office-based)\b'
        }
        
        # Also check the location field for work type indicators
        if '(remote)' in text_lower or 'remote' in text_lower:
            return 'remote'
        elif '(hybrid)' in text_lower or 'hybrid' in text_lower:
            return 'hybrid'
        
        for work_type, pattern in patterns.items():
            if re.search(pattern, text_lower):
                return work_type
        
        return None

    def _extract_employment_type(self, text: str) -> Optional[str]:
        """Extract employment type with enhanced patterns"""
        if not text or not isinstance(text, str):
            return None
            
        text_lower = text.lower()
        patterns = {
            'full-time': r'\b(?:full-?time|permanent|regular|full time)\b',
            'part-time': r'\b(?:part-?time|casual|part time)\b',
            'contract': r'\b(?:contract|contractor|freelance|temporary|project-based)\b',
            'internship': r'\b(?:intern|internship|trainee|graduate program)\b'
        }
        
        for emp_type, pattern in patterns.items():
            if re.search(pattern, text_lower):
                return emp_type
        
        # Default assumption for developer roles
        if any(term in text_lower for term in ['developer', 'engineer', 'programmer']):
            return 'full-time'
        
        return None

    def _extract_experience_level(self, text: str) -> Optional[str]:
        """Extract experience level with enhanced patterns"""
        if not text or not isinstance(text, str):
            return None
            
        text_lower = text.lower()
        
        # Check job title first
        if 'senior' in text_lower or 'sr.' in text_lower:
            return 'senior'
        elif 'junior' in text_lower or 'jr.' in text_lower:
            return 'entry'
        elif 'lead' in text_lower or 'principal' in text_lower:
            return 'senior'
        
        # Pattern matching in description
        patterns = {
            'entry': r'\b(?:entry.level|junior|graduate|0.2 years?|fresh|new grad)\b',
            'mid': r'\b(?:mid.level|intermediate|3.5 years?|2.7 years?)\b',
            'senior': r'\b(?:senior|lead|6\+ years?|5\+ years?|8\+ years?)\b',
            'executive': r'\b(?:director|manager|head|chief|executive|principal)\b'
        }
        
        for level, pattern in patterns.items():
            if re.search(pattern, text_lower):
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
            '[data-automation*="salary"]',
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
        
    def _parse_salary_text(self, salary_text: str) -> Dict[str, Any]:
        for pattern in self.salary_patterns:
            match = pattern.search(salary_text)
            if match:
                return {
                    'min': self._parse_salary_number(match.group(1)),
                    'max': self._parse_salary_number(match.group(2)) if len(match.groups()) > 1 else None,
                    'currency': 'PHP',
                    'period': 'monthly'
                }
        return {'min': None, 'max': None, 'currency': None, 'period': None}
    
    def _extract_benefits(self, text: str) -> List[str]:
        """Extract benefits from text with null safety"""
        if not text or not isinstance(text, str):
            return []
            
        benefit_keywords = [
            'health insurance', 'medical insurance', 'dental coverage', 'life insurance',
            '13th month', 'christmas bonus', 'performance bonus', 'annual leave',
            'sick leave', 'vacation leave', 'training', 'professional development'
        ]
        
        found_benefits = []
        text_lower = text.lower()
        
        for benefit in benefit_keywords:
            if benefit in text_lower:
                found_benefits.append(benefit.title())
        
        return list(set(found_benefits))
    
    def _extract_posting_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract posting date from structured data"""
        date_selectors = [
            '[data-automation*="date"]',
            '[datetime]', 'time[datetime]',
            '.posting-date', '.date-posted'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                date_str = element.get('datetime') or element.get_text(strip=True)
                try:
                    # Try multiple date formats
                    formats = ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%d/%m/%Y', '%m/%d/%Y']
                    for fmt in formats:
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
                except Exception as e:
                    logging.warning(f"Error parsing date '{date_str}': {str(e)}")
                    return None
        
        return None
    
    def _calculate_quality_score(self, data: ExtractedJobData) -> float:
        score = 0.0
        max_score = 10.0
        
        if data.job_title: score += 2.0
        if data.company_name: score += 2.0
        
        if data.location: score += 1.0
        if data.work_type: score += 1.0
        if data.employment_type: score += 1.0
        
        if data.technical_skills and len(data.technical_skills) > 0: score += 1.0
        if data.experience_level: score += 1.0
        
        if data.salary_min or data.salary_max: score += 0.5
        if data.benefits and len(data.benefits) > 0: score += 0.5
        
        return round(score / max_score, 2)