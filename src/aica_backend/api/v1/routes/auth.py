from fastapi import APIRouter, Depends, HTTPException, status, Request,Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....database.repositories.user import UserCRUD
from ....core.security import verify_password, token_manager, security_validator
from ....core.rate_limiter import rate_limiter
from ....core.config import settings
from .. import schemas
from ... import dependencies
from ....database import models

router = APIRouter()

def _handle_failed_login(identifier: str, detail: str = "Invalid email or password"):
    rate_limiter.record_failed_attempt(identifier)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )
    
def _create_auth_response(user: models.User, response: Response) -> dict:
    token_data = {"sub": user.email, "user_id": user.id}
    access_token = token_manager.create_access_token(token_data)
    refresh_token = token_manager.create_refresh_token(token_data)
    
    cookie_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    refresh_max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS* 24 * 60 * 60
    
    cookie_settings = {
        "httponly": True,
        "secure": settings.ENVIRONMENT == "production",
        "samesite": "strict",
    }
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=cookie_max_age,
        path="/",
        **cookie_settings
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=refresh_max_age,
        path="/api/v1/refresh",
        **cookie_settings
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": cookie_max_age
    }
    
@router.post('/login/access-token', response_model=schemas.token.Token)
def login_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
        Authenticate user and return access token.
    """
    
    if hasattr(request.app.state, 'limiter'):
        request.app.state.limiter.limit("5/minute")(request)
    
    client_ip = request.client.host
    email = security_validator.sanitize_email(form_data.username)
    identifier = f"{email}:{client_ip}"
    
    if not rate_limiter.check_rate_limit(identifier):
        remaining_time = rate_limiter.get_lockout_time_remaining(identifier)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many failed login attempts. Try again in {remaining_time // 60} seconds.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not security_validator.validate_email_format(email):
        _handle_failed_login(identifier)
    
    # Authenticate user
    db_user = UserCRUD.get_user_by_email(db, email=email)
    
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        _handle_failed_login(identifier)
    
    # Clear failed attempts on successful login
    rate_limiter.clear_failed_attempts(identifier)
    
    return _create_auth_response(db_user, response)

@router.post('/refresh', response_model=schemas.token.Token)
def refresh_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    payload = token_manager.verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    email = payload.get("sub")
    db_user = UserCRUD.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return _create_auth_response(db_user, response)

@router.post('/logout')
def logout(
    request: Request,
    response: Response,
    current_user: models.User = Depends(dependencies.get_current_user)
):
    token = dependencies.extract_token_from_request(request)
    if token:
        token_manager.blacklist_token(token)
        
    # Clear cookies
    cookie_settings = {
        "httponly": True,
        "secure": settings.ENVIRONMENT == "production",
        "samesite": "strict",
    }
    
    response.delete_cookie("access_token", path="/", **cookie_settings)
    response.delete_cookie("refresh_token", path="/api/v1/refresh", **cookie_settings)
    
    return {"message": "Successfully logged out"}

@router.get("/verify")
def verfify_token(
    current_user: models.User = Depends(dependencies.get_current_user)
):
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email
        }
    }
    