from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Date, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base_class import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    profile: Mapped["Profile"] = relationship(back_populates="user", cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    # Personal Details
    first_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    professional_title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    contact_number: Mapped[str] = mapped_column(String, index=True, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)
    linkedin_url: Mapped[str] = mapped_column(String, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="profile")
    educations: Mapped[list["Education"]] = relationship(cascade="all, delete-orphan")
    experiences: Mapped[list["Experience"]] = relationship(cascade="all, delete-orphan")
    skills: Mapped[list["Skill"]] = relationship(secondary="profile_skill_link", back_populates="profiles")
    certificates: Mapped[list["Certificate"]] = relationship(cascade="all, delete-orphan")

class Education(Base):
    __tablename__ = "educations"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    institution_name: Mapped[str] = mapped_column(String, nullable=False)
    degree: Mapped[str] = mapped_column(String, nullable=False)
    field_of_study: Mapped[str] = mapped_column(String)
    start_date: Mapped[datetime.date] = mapped_column(Date)
    end_date: Mapped[datetime.date] = mapped_column(Date)

class Experience(Base):
    __tablename__ = "experiences"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    job_title: Mapped[str] = mapped_column(String, nullable=True)
    company_name: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime.date] = mapped_column(Date)
    end_date: Mapped[datetime.date] = mapped_column(Date)
    description: Mapped[list[str]] = mapped_column(JSON, nullable=True)

class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    profiles: Mapped[list["Profile"]] = relationship(secondary="profile_skill_link", back_populates="skills")

class ProfileSkillLink(Base):
    __tablename__ = "profile_skill_link"
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

class Certificate(Base):
    __tablename__ = "certificates"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    issuing_organization: Mapped[str] = mapped_column(String)
    issue_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
