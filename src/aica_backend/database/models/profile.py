import datetime

from sqlalchemy import String, DateTime, Date, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base_class import Base
from typing import List, Optional

class Profile(Base):
    __tablename__ = "profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    
    first_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    professional_title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    contact_number: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    profile_picture: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )
    
    user: Mapped["User"] = relationship(back_populates="profile")
    educations: Mapped[List["Education"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="profile"
    )
    experiences: Mapped[List["Experience"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="profile"
    )
    certificates: Mapped[List["Certificate"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="profile"
    )
    skills: Mapped[List["Skill"]] = relationship(
        secondary="profile_skill_link",
        back_populates="profiles"
    )
    
class Education(Base):
    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    institution_name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    degree: Mapped[str] = mapped_column(String(100), nullable=False)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="educations")

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    job_title: Mapped[str] = mapped_column(String(200), nullable=False)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="experiences")

class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False)

    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    issuing_organization: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    issue_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[Optional[datetime.date]] = mapped_column(Date, nullable=True)
    credential_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    credential_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="certificates")