from typing import Optional, List
from pydantic import BaseModel, constr
from datetime import datetime, date

# Education schemas
class EducationBase(BaseModel):
    institution_name: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    institution_name: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class Education(EducationBase):
    id: int
    profile_id: int
    
    class Config:
        from_attributes = True

# Experience schemas
class ExperienceBase(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[List[str]] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[List[str]] = None

class Experience(ExperienceBase):
    id: int
    profile_id: int
    
    class Config:
        from_attributes = True

# Skill schemas
class Skill(BaseModel):
    name: str
    class Config:
        from_attributes = True
    
class SkillBase(BaseModel):
    name: constr(min_length=1, strip_whitespace=True) # type: ignore

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    
    class Config:
        from_attributes = True

# Certificate schemas
class CertificateBase(BaseModel):
    name: str
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None

class CertificateCreate(CertificateBase):
    pass

class CertificateUpdate(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None

class Certificate(CertificateBase):
    id: int
    profile_id: int
    
    class Config:
        from_attributes = True

# Profile schemas
class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    professional_title: str
    contact_number: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    summary: Optional[str] = None

class ProfileCreate(ProfileBase):
    educations: List[EducationCreate] = []
    experiences: List[ExperienceCreate] = []
    skills: List[str] = []
    certificates: List[CertificateCreate] = []

class ProfileUpdate(ProfileBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    professional_title: Optional[str] = None
    contact_number: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    summary: Optional[str] = None

class ProfileInDBBase(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Profile(ProfileInDBBase):
    educations: List[Education] = []
    experiences: List[Experience] = []
    skills: List[Skill] = []
    certificates: List[Certificate] = []

class ProfileInDB(ProfileInDBBase):
    pass

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