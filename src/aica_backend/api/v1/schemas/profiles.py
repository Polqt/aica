from typing import List, Optional
from pydantic import BaseModel, constr, Field, EmailStr, conlist, field_validator
from datetime import datetime, date

# Education
class EducationBase(BaseModel):
    institution_name: str
    address: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: date
    description: str

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_dates(cls, v):
        """
        VALIDATION FIX: Parse various date formats to ensure consistency
        
        PROBLEM: Frontend might send dates in different formats:
        - MM/DD/YYYY (from date pickers)
        - DD/MM/YYYY (locale-specific)
        - ISO strings
        
        SOLUTION: Accept string dates and convert them to Python date objects
        Only accept YYYY-MM-DD format to maintain data consistency
        """
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Invalid date format, expected YYYY-MM-DD')
        return v

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    institution_name: Optional[str] = None
    address: Optional[str] = None
    degree: str
    field_of_study: str
    start_date: date
    end_date: date
    description: str

class Education(EducationBase):
    id: int
    profile_id: int
    class Config:
        from_attributes = True


# Experience
class ExperienceBase(BaseModel):
    job_title: str
    company_name: str
    start_date: date
    end_date: date
    description: List[str]
    is_current: bool = False

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_dates(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Invalid date format, expected YYYY-MM-DD')
        return v

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[List[str]] = None
    is_current: Optional[bool] = None

class Experience(ExperienceBase):
    id: int
    profile_id: int
    class Config:
        from_attributes = True


# Skill
class SkillBase(BaseModel):
    name: constr(min_length=1, strip_whitespace=True)  # type: ignore

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    class Config:
        from_attributes = True


# Certificate
class CertificateBase(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    credential_url: Optional[str] = None
    credential_id: Optional[str] = None

    @field_validator('issue_date', mode='before')
    @classmethod
    def parse_issue_date(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Invalid date format, expected YYYY-MM-DD')
        return v

class CertificateCreate(CertificateBase):
    pass

class CertificateUpdate(CertificateBase):
    pass

class Certificate(CertificateBase):
    id: int
    profile_id: int
    class Config:
        from_attributes = True


# Profile
class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    professional_title: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    summary: Optional[str] = None
    profile_picture: Optional[str] = None

class ProfileCreate(ProfileBase):
    first_name: str
    last_name: str
    professional_title: str
    contact_number: str
    address: str
    summary: str
    linkedin_url: Optional[str] = None
    profile_picture: Optional[str] = None

    educations: conlist(EducationCreate, min_length=1)
    experiences: conlist(ExperienceCreate, min_length=1)
    skills: conlist(SkillCreate, min_length=1)
    certificates: conlist(CertificateCreate, min_length=1)

class ProfileUpdate(ProfileBase):
    educations: Optional[List[EducationCreate]] = None
    experiences: Optional[List[ExperienceCreate]] = None
    skills: Optional[List[SkillCreate]] = None
    certificates: Optional[List[CertificateCreate]] = None

class ProfileInDBBase(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Profile(ProfileInDBBase):
    educations: List[Education]
    experiences: List[Experience]
    skills: List[Skill]
    certificates: List[Certificate]

class ProfileWithRelations(Profile):
    pass

class ProfileSummary(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    professional_title: str

    class Config:
        from_attributes = True


# User
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True
