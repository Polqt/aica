from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from ..db.session import SessionLocal
from ..db import models
from ..crud import crud_user
from ..core.config import settings
from .v1.schemas import token as token_schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token", auto_error=False)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def get_token_from_cookie_or_header(request: Request, token: str = Depends(oauth2_scheme)) -> str:
    """
    Get JWT token from httpOnly cookie or Authorization header.
    Cookie takes precedence for security.
    """
    # First try to get token from httpOnly cookie
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        # Remove "Bearer " prefix if present
        if cookie_token.startswith("Bearer "):
            return cookie_token[7:]
        return cookie_token
    
    # Fall back to Authorization header
    if token:
        return token
    
    # No token found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(
    request: Request,
    db: Session = Depends(get_db), 
    token: str = Depends(get_token_from_cookie_or_header)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        token_data = token_schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user_by_email(db, email=token_data.email)

    if user is None:
        raise credentials_exception
    return user