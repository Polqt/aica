from fastapi import HTTPException, status, Request
from fastapi.security.utils import get_authorization_scheme_param
from typing import Optional
import logging

from ..database.session import SessionLocal
from ..database import models
from ..database.repositories.user import UserCRUD
from ..core.security import token_manager

logger = logging.getLogger(__name__)

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
    logger.info(f"get_current_user called for path: {request.url.path}")
    
    # Middleware-provided user
    if getattr(request.state, 'is_authenticated', False) and hasattr(request.state, 'user'):
        user = getattr(request.state, 'user', None)
        if user:
            logger.info(f"User found in middleware state: {user.email}")
            return user
    token = extract_token_from_request(request)
    logger.info(f"Token extracted: {'Present' if token else 'Missing'}")
    
    if not token:
        logger.warning("No authentication token found")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={'WWW-Authenticate': 'Bearer'})
    
    payload = token_manager.verify_token(token, token_type="access")
    logger.info(f"Token verification result: {'Valid' if payload else 'Invalid'}")
    
    if not payload:
        logger.warning("Token verification failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={'WWW-Authenticate': 'Bearer'})
    
    email = payload.get("sub")
    if not email:
        logger.warning("No email found in token payload")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload", headers={'WWW-Authenticate': 'Bearer'})
    
    with SessionLocal() as db:
        user = UserCRUD.get_user_by_email(db, email=email)
        if not user:
            logger.warning(f"User not found in database: {email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={'WWW-Authenticate': 'Bearer'})
        
        logger.info(f"User successfully authenticated: {user.email}")
        return user

def get_optional_current_user(request: Request) -> Optional[models.User]:
    if getattr(request.state, 'is_authenticated', False) and hasattr(request.state, 'user'):
        return request.state.user
    
    return None
