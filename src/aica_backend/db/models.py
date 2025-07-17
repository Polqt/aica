from sqlalchemy import String, DateTime, Date, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from .base_class import Base
import datetime
from typing import List

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

    profile: Mapped["Profile"] = relationship(back_populates="user", cascade="all, delete-orphan", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    first_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    professional_title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    contact_number: Mapped[str] = mapped_column(String, index=True, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    linkedin_url: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    profile_picture: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    educations: Mapped[List["Education"]] = relationship(cascade="all, delete-orphan")
    experiences: Mapped[List["Experience"]] = relationship(cascade="all, delete-orphan")
    certificates: Mapped[List["Certificate"]] = relationship(cascade="all, delete-orphan")
    skills: Mapped[List["Skill"]] = relationship(secondary="profile_skill_link", back_populates="profiles")

class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    institution_name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    degree: Mapped[str] = mapped_column(String, nullable=False)
    field_of_study: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    job_title: Mapped[str] = mapped_column(String, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[List[str]] = mapped_column(JSON, nullable=False)

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    profiles: Mapped[List["Profile"]] = relationship(secondary="profile_skill_link", back_populates="skills")


class ProfileSkillLink(Base):
    __tablename__ = "profile_skill_link"

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    issuing_organization: Mapped[str] = mapped_column(String, nullable=False)
    issue_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    credential_url: Mapped[str] = mapped_column(String, nullable=False)
    credential_id: Mapped[str] = mapped_column(String, nullable=False)

class JobPosting(Base):
    __tablename__ = "job_postings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_url = Mapped[str] = mapped_column(String, unique=True, index=True)
    source_site = Mapped[str] = mapped_column(String, index=True)

    full_text: Mapped[str] = mapped_column(Text, nullable=True)

    job_title: Mapped[str] = mapped_column(String, nullable=True, index=True)
    company_name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    extracted_skills: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=True)
    status: Mapped[str] = mapped_column(String, default="raw", index=True)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)