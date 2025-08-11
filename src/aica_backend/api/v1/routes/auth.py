from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....database.repositories.user import UserCRUD
from ....core.security import verify_password, token_manager, security_validator
from ....core.rate_limiter import rate_limiter
from ....core.config import settings
from .. import schemas
from ... import dependencies

router = APIRouter()


@router.post('/login/access-token', response_model=schemas.token.Token)
def login_for_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Authenticate user and return access token."""
    if hasattr(request.app.state, 'limiter'):
        request.app.state.limiter.limit("5/minute")(request)
    
    client_ip = request.client.host
    email = security_validator.sanitize_email(form_data.username)
    identifier = f"{email}:{client_ip}"
    
    # Check rate limiting
    if not rate_limiter.check_rate_limit(identifier):
        remaining_time = rate_limiter.get_lockout_time_remaining(identifier)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Please try again in {remaining_time // 60} minutes.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate email format
    if not security_validator.validate_email_format(email):
        rate_limiter.record_failed_attempt(identifier)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Authenticate user
    db_user = UserCRUD.get_user_by_email(db, email=email)
    
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        rate_limiter.record_failed_attempt(identifier)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    rate_limiter.clear_failed_attempts(identifier)

    # Create tokens
    token_data = {"sub": db_user.email, "user_id": db_user.id}
    access_token = token_manager.create_access_token(data=token_data)
    refresh_token = token_manager.create_refresh_token(data=token_data)
    
    cookie_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    # Set secure cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=cookie_max_age,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        path="/",
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
        path="/api/v1/refresh",
    )
    
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
    """Refresh access token using refresh token."""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = token_manager.verify_token(refresh_token, token_type="refresh")
    if not payload:
        response.delete_cookie("refresh_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("sub")
    db_user = UserCRUD.get_user_by_email(db, email=email)
    if not db_user:
        response.delete_cookie("refresh_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {"sub": db_user.email, "user_id": db_user.id}
    new_access_token = token_manager.create_access_token(data=token_data)
    
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
    """Logout user and blacklist token."""
    token = dependencies.get_token_from_cookie_or_header(request)
    if token:
        token_manager.blacklist_token(token)
    
    # Clear cookies
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
    
    return {"message": "Successfully logged out"}


@router.get('/verify')
def verify_token(
    current_user: dict = Depends(dependencies.get_current_user)
):
    """Verify current token and return user info."""
    return {
        "valid": True,
        "user": {
            "id": current_user.get("id"),
            "email": current_user.get("email")
        }
    }