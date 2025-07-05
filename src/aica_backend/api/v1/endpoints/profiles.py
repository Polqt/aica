from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....db import models
from ....crud import crud_profile
from .. import schemas
from ... import dependencies

router = APIRouter()

@router.get("/profile", response_model=schemas.profiles.Profile)
def read_current_user_profile(current_user: models.User = Depends(dependencies.get_current_user)):
    profile = crud_profile.get_profile(current_user)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found for this user.")
    
    return profile

@router.put('/profile', response_model=schemas.profiles.Profile)
def update_current_user_profile(profile_in: schemas.profiles.ProfileUpdate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    profile = crud_profile.update_profile(db=db, user=current_user, profile_in=profile_in)
    
    return profile
