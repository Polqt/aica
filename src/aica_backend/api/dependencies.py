from fastapi import HTTPException, status, Request
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional

from database.session import SessionLocal
from database import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def extract_token_from_request(request: Request) -> Optional[str]:
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        if cookie_token.startswith("Bearer "):
            return cookie_token[7:]
        return cookie_token
    
    authorization = request.headers.get("Authorization")
    if authorization:
        scheme, token = get_authorization_scheme_param(authorization)
        if scheme.lower() == "bearer":
            return token
    return None
    
def get_current_user(request: Request) -> models.User:
    if not getattr(request.state, 'is_authenticated', False) or not hasattr(request.state, 'user'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    user = getattr(request.state, 'user', None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    return user

def get_optional_current_user(request: Request) -> Optional[models.User]:
    if getattr(request.state, 'is_authenticated', False) and hasattr(request.state, 'user'):
        return request.state.user
    
    return None
