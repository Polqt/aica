from typing import List, Optional
from pydantic import BaseModel, constr, Field, field_validator
from datetime import datetime, date
from ....utils.date_validator import parse_date_string

# Education
class EducationBase(BaseModel):
    institution_name: str
    address: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: date
    end_date: date
    description: Optional[str] = None

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_dates(cls, v):
        if isinstance(v, str) and len(v) == 7:
            v = f"{v}-01"
        return parse_date_string(v)

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    institution_name: Optional[str] = None
    address: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

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
    end_date: Optional[date] = None
    description: Optional[List[str]] = Field(default=[], description="Job responsibilities")
    is_current: bool = False

    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_dates(cls, v):
        return parse_date_string(v)

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
        return parse_date_string(v)

class CertificateCreate(CertificateBase):
    pass

class CertificateUpdate(CertificateBase):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None

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

    educations: List[EducationCreate] = Field(..., min_length=1)
    experiences: List[ExperienceCreate] = Field(default=[], description="Work experience (optional)")
    skills: List[SkillCreate] = Field(..., min_length=1)
    certificates: List[CertificateCreate] = Field(default=[], description="Certificates (optional)")

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

class ProfileFlags(BaseModel):
    has_experiences: bool
    has_certificates: bool

class ProfileCompletionStatus(BaseModel):
    """Schema for profile completion status tracking"""
    is_profile_created: bool
    completed_steps: List[str]  # ["profile", "education", "skills", "experience", "certificates"]
    next_required_step: str  # "profile", "education", "skills", "experience", "certificates", or "complete"
    overall_completion_percentage: int  # 0-100
    