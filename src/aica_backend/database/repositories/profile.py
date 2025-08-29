from sqlalchemy.orm import Session
from .. import models
from ...api.v1.schemas import profiles as profile_schemas


def get_or_create_skill(db: Session, skill_name: str) -> models.Skill:
    skill = db.query(models.Skill).filter(models.Skill.name == skill_name).first()

    if not skill:
        skill = models.Skill(name=skill_name)
        db.add(skill)
    return skill

def update_profile(db: Session, user: models.User, profile_in: profile_schemas.ProfileUpdate) -> models.Profile:
    # Rehydrate/resolve profile via the current db session to avoid detached instances
    profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    if not profile:
        profile = models.Profile(user_id=user.id)
        db.add(profile)

    # Update basic profile fields (excluding relations)
    profile_data = profile_in.model_dump(exclude_unset=True)

    for field, value in profile_data.items():
        if field not in ["skills", "educations", "experiences", "certificates"]:
            setattr(profile, field, value)

    # Handle skills update
    if profile_in.skills is not None:
        # Extract skill names from SkillCreate objects
        skill_names = [skill.name for skill in profile_in.skills]
        profile.skills = [get_or_create_skill(db, name) for name in skill_names]

    # Handle educations update (required field)
    if profile_in.educations is not None:
        profile.educations.clear()
        for edu in profile_in.educations:
            edu_data = edu.model_dump(exclude={'profile_id'})
            new_edu = models.Education(**edu_data)
            profile.educations.append(new_edu)

    # Handle experiences update (It can be empty)
    if profile_in.experiences is not None:
        profile.experiences.clear()
        for exp in profile_in.experiences:
            exp_data = exp.model_dump(exclude={'profile_id'})
            new_exp = models.Experience(**exp_data)
            profile.experiences.append(new_exp)

    # Handle certificates update (It can be empty)
    if profile_in.certificates is not None:
        profile.certificates.clear()
        for cert in profile_in.certificates:
            cert_data = cert.model_dump(exclude={'profile_id'})
            new_cert = models.Certificate(**cert_data)
            profile.certificates.append(new_cert)

    db.commit()
    db.refresh(profile)
    return profile

def get_profile(user: models.User) -> models.Profile:
    return user.profile