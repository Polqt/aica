import logging

from typing import Optional, Set
from fastapi import Request
from jose import jwt, JWTError

from ...api.dependencies import extract_token_from_request
from ...database import models
from ...core.config import settings
from ...database.repositories.user import UserCRUD
from ...database.session import SessionLocal

logger = logging.getLogger(__name__)

class AuthMiddleware:
    PUBLIC_PATHS: Set[str] = {
        "/docs", "/redoc", "/openapi.json", "/health", "/",
        "/api/v1/users/", "/api/v1/login/access-token", "/api/v1/logout"
    }
    
    def __init__(self):
        pass
    
    async def __call__(self, request: Request, call_next):
        if self._is_public_path(request.url.path):
            return await call_next(request)
        
        # Extract and validate token
        token = self._extract_token(request)
        user = await self._validate_token(token) if token else None
        
        # Set request state
        request.state.is_authenticated = user is not None
        if user:
            request.state.user = user
        
        return await call_next(request)

    def _is_public_path(self, path: str) -> bool:
        return any(path.startswith(public_path) for public_path in self.PUBLIC_PATHS)
    
    def _extract_token(self, request: Request) -> Optional[str]:
        return extract_token_from_request(request)
    
    async def _validate_token(self, token: str) -> Optional[models.User]:
        if not token:
            return None
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            email: str = payload.get("sub")
            if not email:
                logger.warning("Token payload missing 'sub' field")
                return None
            
            with SessionLocal() as db:
                db_user = UserCRUD.get_user_by_email(db, email=email)
                if not db_user:
                    logger.warning(f"User not found for email: {email}")
                    return None
                
                return db_user
        except JWTError as e:
            logger.warning(f"Token validation error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {e}") 
            return None       