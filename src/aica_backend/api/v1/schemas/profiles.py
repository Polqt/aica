from typing import List
from pydantic import BaseModel, constr, Field, EmailStr, conlist
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

class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    institution_name: str
    address: str
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

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    job_title: str
    company_name: str
    start_date: date
    end_date: date
    description: List[str]
    is_current: bool = False

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
    name: str
    issuing_organization: str
    issue_date: date
    credential_url: str
    credential_id: str

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
    first_name: str
    last_name: str
    professional_title: str
    contact_number: str
    address: str
    linkedin_url: str
    summary: str

class ProfileCreate(ProfileBase):
    educations: conlist(EducationCreate, min_length=1)
    experiences: conlist(ExperienceCreate, min_length=1)
    skills: conlist(SkillCreate, min_length=1)
    certificates: conlist(CertificateCreate, min_length=1)

class ProfileUpdate(ProfileBase):
    educations: conlist(EducationCreate, min_length=1)
    experiences: conlist(ExperienceCreate, min_length=1)
    skills: conlist(SkillCreate, min_length=1)
    certificates: conlist(CertificateCreate, min_length=1)

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
