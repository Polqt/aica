import re
from typing import Tuple, Optional, Dict, Any
from datetime import datetime, date


class ValidationUtils:
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    PHONE_PATTERN = re.compile(
        r'^\+?[\d\s\-\(\)]+$'
    )
    URL_PATTERN = re.compile(
        r'^https?:\/\/(?:[-\w.])+(?:\:[0-9]+)?(?:\/(?:[\w\/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    )
    
    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, Optional[str]]:
        if not email:
            return False, "Email is required"
        
        if not cls.EMAIL_PATTERN.match(email):
            return False, "Invalid email format"
        
        if len(email) > 254: 
            return False, "Email address too long"
        
        return True, None
    
    @classmethod
    def validate_phone(cls, phone: str) -> Tuple[bool, Optional[str]]:
        if not phone:
            return False, "Phone number is required"
        
        clean_phone = re.sub(r'\s', '', phone)
        
        if len(clean_phone) < 10:
            return False, "Phone number too short"
        
        if len(clean_phone) > 15:  
            return False, "Phone number too long"
        
        if not cls.PHONE_PATTERN.match(phone):
            return False, "Invalid phone number format"
        
        return True, None
    
    @classmethod
    def validate_url(cls, url: str) -> Tuple[bool, Optional[str]]:
        if not url:
            return True, None 
        
        if not cls.URL_PATTERN.match(url):
            return False, "Invalid URL format"
        
        if len(url) > 2048:  # Common browser limit
            return False, "URL too long"
        
        return True, None
    
    @classmethod
    def validate_date_range(cls, start_date: date, end_date: Optional[date]) -> Tuple[bool, Optional[str]]:
        if not start_date:
            return False, "Start date is required"
        
        if start_date > date.today():
            return False, "Start date cannot be in the future"
        
        if end_date:
            if end_date < start_date:
                return False, "End date must be after start date"
            
            if end_date > date.today():
                return False, "End date cannot be in the future"
        
        return True, None
    
    @classmethod
    def validate_text_length(cls, text: str, field_name: str, min_length: int = 0, max_length: int = 1000) -> Tuple[bool, Optional[str]]:
        if not text and min_length > 0:
            return False, f"{field_name} is required"
        
        if text and len(text.strip()) < min_length:
            return False, f"{field_name} must be at least {min_length} characters"
        
        if text and len(text) > max_length:
            return False, f"{field_name} must not exceed {max_length} characters"
        
        return True, None
    
    @classmethod
    def validate_profile_data(cls, profile_data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        errors = {}
    
        required_fields = {
            'first_name': (1, 100),
            'last_name': (1, 100),
            'professional_title': (1, 200),
            'summary': (10, 2000),
        }
        
        for field, (min_len, max_len) in required_fields.items():
            value = profile_data.get(field, '')
            is_valid, error = cls.validate_text_length(value, field.replace('_', ' ').title(), min_len, max_len)
            if not is_valid:
                errors[field] = error
        
        if 'email' in profile_data:
            is_valid, error = cls.validate_email(profile_data['email'])
            if not is_valid:
                errors['email'] = error
        
        if 'contact_number' in profile_data:
            is_valid, error = cls.validate_phone(profile_data['contact_number'])
            if not is_valid:
                errors['contact_number'] = error
        
        if 'linkedin_url' in profile_data:
            is_valid, error = cls.validate_url(profile_data['linkedin_url'])
            if not is_valid:
                errors['linkedin_url'] = error
        
        address = profile_data.get('address', '')
        is_valid, error = cls.validate_text_length(address, 'Address', 5, 500)
        if not is_valid:
            errors['address'] = error
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_experience_data(cls, experience_data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        errors = {}
        
        job_title = experience_data.get('job_title', '')
        is_valid, error = cls.validate_text_length(job_title, 'Job Title', 1, 200)
        if not is_valid:
            errors['job_title'] = error
        
        company_name = experience_data.get('company_name', '')
        is_valid, error = cls.validate_text_length(company_name, 'Company Name', 1, 200)
        if not is_valid:
            errors['company_name'] = error
        
        start_date = experience_data.get('start_date')
        end_date = experience_data.get('end_date')
        is_current = experience_data.get('is_current', False)
        
        if start_date:
            if isinstance(start_date, str):
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                except ValueError:
                    errors['start_date'] = "Invalid date format, use YYYY-MM-DD"
                    start_date = None
            
            if end_date and isinstance(end_date, str):
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                except ValueError:
                    errors['end_date'] = "Invalid date format, use YYYY-MM-DD"
                    end_date = None
                    
            if start_date and not is_current:
                is_valid, error = cls.validate_date_range(start_date, end_date)
                if not is_valid:
                    errors['date_range'] = error
        else:
            errors['start_date'] = "Start date is required"
        
        return len(errors) == 0, errors
