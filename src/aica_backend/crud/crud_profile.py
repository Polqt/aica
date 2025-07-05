from sqlalchemy.orm import Session
from ..db import models
from ..api.v1.schemas import profiles as profile_schemas


def get_or_create_skill(db: Session, skill_name: str) -> models.Skill:
    skill = db.query(models.Skill).filter(models.Skill.name == skill_name).first()

    if not skill:
        skill = models.Skill(name=skill_name)
        db.add(skill)
        db.commit()
        db.refresh(skill)
    return skill

def update_profile(db: Session, user: models.User, profile_in: profile_schemas.ProfileUpdate) -> models.Profile:
    profile = user.profile

    if not profile:
        profile = models.Profile(user=user)
        db.add(profile)

    profile_data = profile_in.model_dump(exclude_unset=True)

    for field, value in profile_data.items():
        if field not in ["skills", "educations", "experiences", "certificates"]:
            setattr(profile, field, value)

    if profile_in.skills is not None:
        profile.skills = [get_or_create_skill(db, name) for name in profile_in.skills]

    if profile_in.educations is not None:
        profile.educations = [models.Education(**edu.model_dump()) for edu in profile_in.educations]

    if profile_in.experiences is not None:
        profile.experiences = [models.Experience(**exp.model_dump()) for exp in profile_in.experiences]

    if profile_in.certificates is not None:
        profile.certificates = [models.Certificate(**cert.model_dump()) for cert in profile_in.certificates]

    db.commit()
    db.refresh(profile)
    return profile

def get_profile(user: models.User) -> models.Profile:
    return user.profile