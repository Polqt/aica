from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base_class import Base
from typing import List, Optional

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)

    profiles: Mapped[List["Profile"]] = relationship(
        secondary="profile_skill_link", 
        back_populates="skills"
    )

class ProfileSkillLink(Base):
    __tablename__ = "profile_skill_link"

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)
    proficiency_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)