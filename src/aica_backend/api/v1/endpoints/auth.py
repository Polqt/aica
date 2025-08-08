from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging
from datetime import datetime, timedelta

from ....crud import crud_user
from ....core.security import (
    create_access_token, 
    verify_password, 
    token_manager,
    security_validator
)
from ....core.config import settings
from .. import schemas
from ... import dependencies

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage for failed login attempts (use Redis in production)
failed_login_attempts = {}

class AuthenticationService:
    """
    Service class for handling authentication operations.
    Centralizes authentication logic with security best practices.
    """
    
    @staticmethod
    def check_rate_limit(request: Request, identifier: str) -> bool:
        """Check if the user/IP has exceeded login attempt limits"""
        now = datetime.utcnow()
        
        # Clean old attempts (older than lockout duration)
        cutoff_time = now - timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
        if identifier in failed_login_attempts:
            failed_login_attempts[identifier] = [
                attempt for attempt in failed_login_attempts[identifier]
                if attempt > cutoff_time
            ]
        
        # Check if user is locked out
        attempts = failed_login_attempts.get(identifier, [])
        if len(attempts) >= settings.MAX_LOGIN_ATTEMPTS:
            return False
        
        return True
    
    @staticmethod
    def record_failed_attempt(identifier: str):
        """Record a failed login attempt"""
        now = datetime.utcnow()
        if identifier not in failed_login_attempts:
            failed_login_attempts[identifier] = []
        failed_login_attempts[identifier].append(now)
    
    @staticmethod
    def clear_failed_attempts(identifier: str):
        """Clear failed login attempts after successful login"""
        if identifier in failed_login_attempts:
            del failed_login_attempts[identifier]

@router.post('/login/access-token', response_model=schemas.token.Token)
def login_for_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Enhanced login endpoint with security features:
    - Rate limiting to prevent brute force attacks
    - Account lockout after multiple failed attempts
    - Secure cookie handling
    - Audit logging
    """
    # Apply rate limiting if available
    if hasattr(request.app.state, 'limiter'):
        request.app.state.limiter.limit("5/minute")(request)
    
    # Get client identifier for rate limiting
    client_ip = request.client.host
    email = security_validator.sanitize_email(form_data.username)
    identifier = f"{email}:{client_ip}"
    
    # Check rate limiting
    if not AuthenticationService.check_rate_limit(request, identifier):
        logger.warning(
            f"Login attempt blocked due to rate limiting: {email} from {client_ip}"
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Please try again in {settings.LOCKOUT_DURATION_MINUTES} minutes.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate email format
    if not security_validator.validate_email_format(email):
        AuthenticationService.record_failed_attempt(identifier)
        logger.warning(f"Invalid email format attempted: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = crud_user.get_user_by_email(db, email=email)
    
    # Verify credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        AuthenticationService.record_failed_attempt(identifier)
        logger.warning(f"Failed login attempt for email: {email} from IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Successful login - clear failed attempts
    AuthenticationService.clear_failed_attempts(identifier)
    
    # Create tokens
    token_data = {"sub": user.email, "user_id": user.id}
    access_token = token_manager.create_access_token(data=token_data)
    refresh_token = token_manager.create_refresh_token(data=token_data)
    
    # Set secure httpOnly cookies
    cookie_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=cookie_max_age,
        httponly=True,  # Prevents JavaScript access
        secure=settings.ENVIRONMENT == "production",  # HTTPS only in production
        samesite="strict",  # CSRF protection
        path="/",  # Cookie available for entire domain
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        path="/api/v1/refresh",  # Only available for refresh endpoint
    )
    
    # Log successful login
    logger.info(f"Successful login: {email} from IP: {client_ip}")
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": cookie_max_age
    }

@router.post('/refresh', response_model=schemas.token.Token)
def refresh_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db)
):
    """
    Refresh access token using refresh token.
    Provides seamless token renewal without user intervention.
    """
    # Get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify refresh token
    payload = token_manager.verify_token(refresh_token, token_type="refresh")
    if not payload:
        response.delete_cookie("refresh_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    email = payload.get("sub")
    user = crud_user.get_user_by_email(db, email=email)
    if not user:
        response.delete_cookie("refresh_token") 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    token_data = {"sub": user.email, "user_id": user.id}
    new_access_token = token_manager.create_access_token(data=token_data)
    
    # Set new access token cookie
    cookie_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_access_token}",
        max_age=cookie_max_age,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        path="/",
    )
    
    logger.info(f"Token refreshed for user: {email}")
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": cookie_max_age
    }

@router.post('/logout')
def logout(
    request: Request,
    response: Response,
    current_user: dict = Depends(dependencies.get_current_user)
):
    """
    Enhanced logout endpoint that:
    - Clears secure httpOnly cookies
    - Blacklists current token to prevent reuse
    - Logs logout activity
    """
    # Get current token for blacklisting
    token = dependencies.get_token_from_cookie_or_header(request)
    if token:
        token_manager.blacklist_token(token)
    
    # Clear authentication cookies
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        path="/",
    )
    
    response.delete_cookie(
        key="refresh_token", 
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        path="/api/v1/refresh",
    )
    
    # Log logout activity
    user_email = current_user.get("email", "unknown")
    logger.info(f"User logged out: {user_email}")
    
    return {"message": "Successfully logged out"}

@router.get('/verify')
def verify_token(
    current_user: dict = Depends(dependencies.get_current_user)
):
    """
    Token verification endpoint.
    Useful for frontend to check if current token is still valid.
    """
    return {
        "valid": True,
        "user": {
            "id": current_user.get("id"),
            "email": current_user.get("email")
        }
    }