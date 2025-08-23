from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from ....core.security import token_manager, security_validator, verify_password
from ....database.repositories.user import UserCRUD
from ....database import models
from .. import schemas
from .. import dependencies

router = APIRouter()

@router.post('/', response_model=schemas.token.Token)
def create_user(
    user_data: schemas.user.UserCreate,
    request: Request,
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
                detail="Failed to create user"
            )
        
        # Generate access token
        token_data = {"sub": new_user.email, "user_id": new_user.id}
        access_token = token_manager.create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
@router.get('/me', response_model=schemas.user.UserResponse)
def get_current_user_info(
    current_user: models.User = Depends(dependencies.get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }

@router.put('/me/password')
def change_password(
    password_data: schemas.user.PasswordChange,
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        