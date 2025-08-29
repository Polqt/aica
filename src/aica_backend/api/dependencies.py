from fastapi import HTTPException, status, Request
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional

from ..database.session import SessionLocal
from ..database import models
from ..database.repositories.user import UserCRUD
from ..core.security import token_manager

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
    # Middleware-provided user
    if getattr(request.state, 'is_authenticated', False) and hasattr(request.state, 'user'):
        user = getattr(request.state, 'user', None)
        if user:
            return user
    # Fallback: verify token directly
    token = extract_token_from_request(request)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={'WWW-Authenticate': 'Bearer'})
    payload = token_manager.verify_token(token, token_type="access")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={'WWW-Authenticate': 'Bearer'})
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload", headers={'WWW-Authenticate': 'Bearer'})
    with SessionLocal() as db:
        user = UserCRUD.get_user_by_email(db, email=email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={'WWW-Authenticate': 'Bearer'})
        return user

def get_optional_current_user(request: Request) -> Optional[models.User]:
    if getattr(request.state, 'is_authenticated', False) and hasattr(request.state, 'user'):
        return request.state.user
    
    return None
