from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import logging

from ....core.security import token_manager, security_validator
from ....crud import crud_user
from .. import schemas
from ... import dependencies
from ..schemas.token import Token

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post('/', response_model=Token)
def create_user_endpoint(
    user_data: schemas.users.UserCreate, 
    request: Request,
    db: Session = Depends(dependencies.get_db)
):
    """
    Enhanced user registration endpoint with comprehensive security validation.
    Creates new user account and returns authentication token.
    """
    try:
        # Apply rate limiting if available
        if hasattr(request.app.state, 'limiter'):
            request.app.state.limiter.limit("3/minute")(request)
        
        # Get client IP for logging
        client_ip = request.client.host if request.client else "unknown"
        
        # Sanitize and validate email
        sanitized_email = security_validator.sanitize_email(user_data.email)
        
        if not security_validator.validate_email_format(sanitized_email):
            logger.warning(f"Invalid email format in registration: {user_data.email} from IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Check if user already exists
        existing_user = crud_user.get_user_by_email(db, email=sanitized_email)
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {sanitized_email} from IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Validate password strength
        is_valid_password, error_message = security_validator.validate_password_strength(user_data.password)
        if not is_valid_password:
            logger.warning(f"Weak password in registration for {sanitized_email} from IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Create user with validated data
        try:
            new_user = crud_user.create_user(db=db, user=user_data)
        except ValueError as e:
            logger.warning(f"User creation validation error: {str(e)} for {sanitized_email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"User creation error: {str(e)} for {sanitized_email}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user account"
            )
        
        # Create authentication tokens
        token_data = {"sub": new_user.email, "user_id": new_user.id}
        access_token = token_manager.create_access_token(data=token_data)
        
        logger.info(f"New user registered successfully: {sanitized_email} from IP: {client_ip}")
        
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (these are expected errors)
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in user registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )

@router.get('/me', response_model=schemas.users.UserResponse)
def get_current_user_info(
    current_user: dependencies.models.User = Depends(dependencies.get_current_user)
):
    """
    Get current authenticated user information.
    Returns user profile data without sensitive information.
    """
    try:
        return {
            "id": current_user.id,
            "email": current_user.email,
            "created_at": current_user.created_at
        }
    except Exception as e:
        logger.error(f"Error retrieving user info for user ID {current_user.id}: {str(e)}")
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
    """
    Change current user's password with security validation.
    Requires current password verification.
    """
    try:
        # Verify current password
        if not security_validator.verify_password(password_data.current_password, current_user.hashed_password):
            logger.warning(f"Invalid current password attempt for user ID: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password strength
        is_valid_password, error_message = security_validator.validate_password_strength(password_data.new_password)
        if not is_valid_password:
            logger.warning(f"Weak password change attempt for user ID: {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Check if new password is different from current
        if security_validator.verify_password(password_data.new_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password"
            )
        
        # Update password
        success = crud_user.UserCRUD.update_user_password(db, current_user.id, password_data.new_password)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        
        logger.info(f"Password changed successfully for user ID: {current_user.id}")
        return {"message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error changing password for user ID {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password change"
        )
