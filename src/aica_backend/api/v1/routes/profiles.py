from fastapi import APIRouter, Depends, HTTPException, status
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
    try:
        # Validate required fields for profile step completion
        if hasattr(profile_in, 'first_name') and profile_in.first_name:
            required_fields = ['first_name', 'last_name', 'professional_title', 'contact_number', 'address', 'summary']
            missing_fields = []

            for field in required_fields:
                if hasattr(profile_in, field):
                    value = getattr(profile_in, field)
                    if not value or (isinstance(value, str) and value.strip() == ""):
                        missing_fields.append(field.replace('_', ' ').title())

            if missing_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required fields: {', '.join(missing_fields)}"
                )

        updated_profile = profile.update_profile(
            db=db,
            user=current_user,
            profile_in=profile_in
        )

        return schemas.profiles.Profile.model_validate(updated_profile)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Profile update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

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

@router.get('/profile/completion-status', response_model=schemas.profiles.ProfileCompletionStatus)
def get_profile_completion_status(
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """Get profile completion status for onboarding flow"""
    user_profile = profile.get_profile(current_user)
    if not user_profile:
        return schemas.profiles.ProfileCompletionStatus(
            is_profile_created=False,
            completed_steps=[],
            next_required_step="profile",
            overall_completion_percentage=0
        )

    completed_steps = []
    total_steps = 5  # profile, education, skills, experience, certificates

    # Check profile completion (required fields)
    required_profile_fields = [
        user_profile.first_name,
        user_profile.last_name,
        user_profile.professional_title,
        user_profile.contact_number,
        user_profile.address,
        user_profile.summary
    ]

    if all(required_profile_fields):
        completed_steps.append("profile")

    # Check education completion (at least one education required)
    if user_profile.educations and len(user_profile.educations) > 0:
        completed_steps.append("education")

    # Check skills completion (at least one skill required)
    if user_profile.skills and len(user_profile.skills) > 0:
        completed_steps.append("skills")

    # Check experience completion (optional)
    if user_profile.experiences and len(user_profile.experiences) > 0:
        completed_steps.append("experience")

    # Check certificates completion (optional)
    if user_profile.certificates and len(user_profile.certificates) > 0:
        completed_steps.append("certificates")

    # Determine next required step
    step_order = ["profile", "education", "skills", "experience", "certificates"]
    next_step = None
    for step in step_order:
        if step not in completed_steps:
            next_step = step
            break

    completion_percentage = int((len(completed_steps) / total_steps) * 100)

    return schemas.profiles.ProfileCompletionStatus(
        is_profile_created=True,
        completed_steps=completed_steps,
        next_required_step=next_step or "complete",
        overall_completion_percentage=completion_percentage
    )
