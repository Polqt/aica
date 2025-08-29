from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session

from ....core.security import security_validator, verify_password
from ....database.repositories.user import UserCRUD
from ....database.repositories import profile
from ....database import models
from .. import schemas
from ... import dependencies
from ..routes.auth import _create_auth_response

router = APIRouter()

@router.post('/', response_model=schemas.users.UserResponse)
def create_user(
    user_data: schemas.users.UserCreate,
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
):
    if hasattr(request.app.state, 'limiter'):
        request.app.state.limiter.limit("5/minute")(request)
        
    try:
        # Check if user already exists
        existing_user = UserCRUD.get_user_by_email(db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create new user
        new_user = UserCRUD.create_user(db, user=user_data)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create account"
            )

        # Create initial empty profile for the user
        try:
            initial_profile = models.Profile(
                user_id=new_user.id,
                first_name="",
                last_name="",
                professional_title="",
                contact_number="",
                address="",
                summary=""
            )
            db.add(initial_profile)
            db.commit()
            db.refresh(new_user)  # Refresh to include the profile relationship
        except Exception as e:
            print(f"Failed to create initial profile: {str(e)}")
            # Don't fail registration if profile creation fails
            db.rollback()

        _create_auth_response(new_user, response)

        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"User creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
@router.get('/me', response_model=schemas.users.UserResponse)
def get_current_user_info(
    current_user: models.User = Depends(dependencies.get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

@router.put('/me/password')
def change_password(
    password_data: schemas.users.PasswordChange,
    current_user: models.User = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db),
):
    try:
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password strength
        is_valid, error_message = security_validator.validate_password_strength(password_data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Check if new password is different
        if verify_password(password_data.new_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from the current password"
            )
        
        # Update password
        success = UserCRUD.update_user_password(db, current_user.id, password_data.new_password)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )

        return {"message": "Password updated successfully"}
    except Exception as e:
        print(f"Password change error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )