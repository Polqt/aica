from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....database import models
from ....database.repositories import profile
from .. import schemas 
from ... import dependencies

router = APIRouter()

@router.get('/profile', response_model=schemas.profiles.Profile)
def read_current_user_profile(
    current_user: models.User = Depends(dependencies.get_current_user),
):
    user_profile = profile.get_profile(current_user)
    if not user_profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )
    
    return schemas.profiles.Profile.model_validate(user_profile)

@router.put('/profile', response_model=schemas.profiles.Profile)
def update_current_user_profile(
    profile_in: schemas.profiles.ProfileUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    updated_profile = profile.update_profile(
        db=db,
        user=current_user,
        profile_in=profile_in
    )
    
    return schemas.profiles.Profile.model_validate(updated_profile)

@router.get('/profile/experiences', response_model=list[schemas.profiles.Experience])
def read_current_user_experiences(
    current_user: models.User = Depends(dependencies.get_current_user),
):
    user_profile = profile.get_profile(current_user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return [schemas.profiles.Experience.model_validate(e) for e in user_profile.experiences or []]

@router.get('/profile/certificates', response_model=list[schemas.profiles.Certificate])
def read_current_user_certificates(
    current_user: models.User = Depends(dependencies.get_current_user),
):
    user_profile = profile.get_profile(current_user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return [schemas.profiles.Certificate.model_validate(c) for c in user_profile.certificates or []]

@router.get('/profile/flags', response_model=schemas.profiles.ProfileFlags)
def read_profile_flags(
    current_user: models.User = Depends(dependencies.get_current_user),
):
    user_profile = profile.get_profile(current_user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return schemas.profiles.ProfileFlags(
        has_experiences=bool(user_profile.experiences),
        has_certificates=bool(user_profile.certificates),
    )

@router.get('/users/me/skills', response_model=list[str])
def read_user_skills(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    rows = db.query(models.UserSkill).filter(models.UserSkill.user_id == current_user.id).all()
    return [r.name for r in rows]
