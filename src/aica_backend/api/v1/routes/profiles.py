from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....database import models
from ....database.repositories import profile
from .. import schemas 
from .. import dependencies

router = APIRouter()

@router.get('/profile', response_model=schemas.prfiles.Profile)
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

