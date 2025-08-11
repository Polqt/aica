from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ....core.security import token_manager, security_validator
from ....database.repositories.user import UserCRUD
from .. import schemas
from ... import dependencies
from ..schemas.token import Token

router = APIRouter()


@router.post('/', response_model=Token)
def create_user_endpoint(
    user_data: schemas.users.UserCreate,
    request: Request,
    db: Session = Depends(dependencies.get_db)
):
    """Create a new user account."""
    try:
        if hasattr(request.app.state, 'limiter'):
            request.app.state.limiter.limit("5/minute")(request)
        
        # Validate and sanitize email
        sanitized_email = security_validator.sanitize_email(user_data.email)
        if not security_validator.validate_email_format(sanitized_email):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid email format"}
            )

        # Check for existing user
        existing_user = UserCRUD.get_user_by_email(db, email=sanitized_email)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "User with this email already exists"}
            )
        
        # Validate password strength
        is_valid_password, error_message = security_validator.validate_password_strength(user_data.password)
        if not is_valid_password:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": error_message}
            )
        
        # Create user
        new_user = UserCRUD.create_user(db=db, user=user_data)
        
        # Generate token
        token_data = {"sub": new_user.email, "user_id": new_user.id}
        access_token = token_manager.create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An internal server error occurred during registration."}
        )


@router.get('/me', response_model=schemas.users.UserResponse)
def get_current_user_info(
    current_user: dependencies.models.User = Depends(dependencies.get_current_user)
):
    """Get current user information."""
    try:
        return {
            "id": current_user.id,
            "email": current_user.email,
            "created_at": current_user.created_at
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )


@router.put('/me/password')
def change_password(
    password_data: schemas.users.PasswordChange,
    current_user: dependencies.models.User = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    """Change user password."""
    try:
        # Import verify_password here to avoid circular imports
        from ....core.security import verify_password
        
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        is_valid_password, error_message = security_validator.validate_password_strength(password_data.new_password)
        if not is_valid_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        if verify_password(password_data.new_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password"
            )
        
        success = UserCRUD.update_user_password(db, current_user.id, password_data.new_password)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        
        return {"message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password change"
        )
