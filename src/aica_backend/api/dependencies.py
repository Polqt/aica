from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from typing import Optional

from ..database.session import SessionLocal
from ..database import models
from ..database.repositories.user import UserCRUD
from ..core.security import token_manager, security_validator
from .v1.schemas import token as token_schema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login/access-token",
    auto_error=False
)

def get_db():
    """Database dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_token_from_cookie_or_header(request: Request, token: str = Depends(oauth2_scheme)) -> str:
    """Extract token from cookie or authorization header."""
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        if cookie_token.startswith("Bearer "):
            token_value = cookie_token[7:]
        else:
            token_value = cookie_token
        
        if len(token_value) < 10:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token_value
    
    # Check for token in Authorization header
    if token:
        if len(token) < 10:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token
    
    # No token found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_cookie_or_header)
) -> models.User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = token_manager.verify_token(token, token_type="access")
        if not payload:
            raise credentials_exception
        
        # Extract and validate email
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        
        if not security_validator.validate_email_format(email):
            raise credentials_exception
        
        token_data = token_schema.TokenData(email=email)
        
    except JWTError:
        raise credentials_exception
    except Exception:
        raise credentials_exception

    try:
        user = UserCRUD.get_user_by_email(db, email=token_data.email)
        if user is None:
            raise credentials_exception
        
        return user
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_optional_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[models.User]:
    """Get current user if authenticated, otherwise return None."""
    try:
        token = get_token_from_cookie_or_header(request)
        return get_current_user(request, db, token)
    except HTTPException:
        return None