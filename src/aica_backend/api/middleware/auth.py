from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError
import logging

from ...core.config import settings
from ...database.session import SessionLocal
from ...database.repositories.user import UserCRUD

logger = logging.getLogger(__name__)

class AuthMiddleware:

    def __init__(self):
        self.public_paths = {
            "/docs", "/redoc", "/openapi.json", "/health", "/",
            "/api/v1/users/", "/api/v1/login/access-token", "/api/v1/logout"
        }
    
    async def __call__(self, request: Request, call_next):
        """Main middleware function that processes each request"""
        if self._is_public_path(request.url.path):
            return await call_next(request)
        
        token = self._extract_token(request)
        if token:
            user = await self._validate_token(token)
            if user:
                request.state.user = user
                request.state.is_authenticated = True
            else:
                request.state.is_authenticated = False
        else:
            request.state.is_authenticated = False
        
        return await call_next(request)
    
    def _is_public_path(self, path: str) -> bool:
        """Check if the request path is a public endpoint that doesn't need authentication"""
        return any(path.startswith(public_path) for public_path in self.public_paths)
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract JWT token from httpOnly cookie or Authorization header"""
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
    
    async def _validate_token(self, token: str) -> Optional[dict]:
        """Validate JWT token and return user data if valid"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            
            email: str = payload.get("sub")
            if not email:
                logger.warning("Token missing subject (email)")
                return None
            
            with SessionLocal() as db:
                db_user = UserCRUD.get_user_by_email(db, email=email)
                if not db_user:
                    logger.warning(f"User not found for email: {email}")
                    return None
                
                return {
                    "id": db_user.id,
                    "email": db_user.email,
                    "created_at": db_user.created_at
                }
                
        except JWTError as e:
            logger.warning(f"JWT validation failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return None

def get_current_user_from_request(request: Request) -> dict:
    if not getattr(request.state, 'is_authenticated', False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return request.state.user
