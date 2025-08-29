"""
Common utility functions used across the AICA backend.
Consolidated from various utility modules to follow DRY principle.
"""

import re
from typing import Optional, List
from datetime import datetime


def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize text by removing extra whitespace.

    Args:
        text: Input text to clean

    Returns:
        Cleaned text string
    """
    if not text or not isinstance(text, str):
        return ''
    return re.sub(r'\s+', ' ', text).strip()


def parse_date_string(date_str: Optional[str]) -> Optional[datetime.date]:
    """
    Parse a date string into a date object.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Date object or None if invalid

    Raises:
        ValueError: If date format is invalid
    """
    if not date_str or date_str == '':
        return None
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Invalid date format, expected YYYY-MM-DD')
    return date_str


def normalize_employment_type(employment_type: Optional[str]) -> str:
    """
    Normalize employment type strings to standard values.

    Args:
        employment_type: Employment type string

    Returns:
        Normalized employment type
    """
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
    """
    Normalize experience level strings to standard values.

    Args:
        experience: Experience level string

    Returns:
        Normalized experience level
    """
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


def clean_skills_array(skills: Optional[List[str]]) -> List[str]:
    """
    Clean and validate a list of skills.

    Args:
        skills: List of skill strings

    Returns:
        Cleaned list of skills
    """
    if not isinstance(skills, list):
        return []

    cleaned_skills = []
    for skill in skills:
        if isinstance(skill, str) and skill.strip():
            cleaned_skill = clean_text(skill)
            if cleaned_skill and len(cleaned_skill) < 50:  # Reasonable length limit
                cleaned_skills.append(cleaned_skill)
    return cleaned_skills[:15]  # Limit to prevent excessive data


def categorize_tech_job(title: str, description: str) -> str:
    """
    Categorize a job as a technology job based on title and description.

    Args:
        title: Job title
        description: Job description

    Returns:
        Technology category string
    """
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


# Error Handling Utilities
class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ValidationError(AppError):
    """Validation error."""
    def __init__(self, message: str):
        super().__init__(message, 400)


class NotFoundError(AppError):
    """Resource not found error."""
    def __init__(self, message: str):
        super().__init__(message, 404)


class ExternalServiceError(AppError):
    """External service error."""
    def __init__(self, message: str):
        super().__init__(message, 502)


def handle_service_error(error: Exception, context: str = "") -> dict:
    """
    Handle service errors consistently.

    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred

    Returns:
        Standardized error response dictionary
    """
    error_msg = f"{context}: {str(error)}" if context else str(error)

    if isinstance(error, ValidationError):
        return {
            "success": False,
            "error": error.message,
            "error_type": "validation_error",
            "status_code": 400
        }
    elif isinstance(error, NotFoundError):
        return {
            "success": False,
            "error": error.message,
            "error_type": "not_found",
            "status_code": 404
        }
    elif isinstance(error, ExternalServiceError):
        return {
            "success": False,
            "error": error.message,
            "error_type": "external_service_error",
            "status_code": 502
        }
    else:
        return {
            "success": False,
            "error": error_msg,
            "error_type": "internal_error",
            "status_code": 500
        }


def create_success_response(data: any = None, message: str = "") -> dict:
    """
    Create a standardized success response.

    Args:
        data: Response data
        message: Optional success message

    Returns:
        Standardized success response dictionary
    """
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    return response