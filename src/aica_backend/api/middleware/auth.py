import logging
from typing import Optional, Set
from fastapi import Request

from ..dependencies import extract_token_from_request
from ...database import models
from ...core.config import settings
from ...database.repositories.user import UserCRUD
from ...database.session import SessionLocal
from jose import jwt, JWTError

logger = logging.getLogger(__name__)

class AuthMiddleware:
    PUBLIC_PATHS: Set[str] = {
        "/docs", "/redoc", "/openapi.json", "/health", "/",
        "/api/v1/login/access-token", "/api/v1/refresh", "/api/v1/logout"
    }
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        if scope['method'] == 'OPTIONS':
            await self.app(scope, receive, send)
            return

        request = Request(scope)

        if self._is_public_path(request.url.path):
            await self.app(scope, receive, send)
            return
        
        token = self._extract_token(request)
        user = await self._validate_token(token) if token else None
        
        scope['state'] = {'is_authenticated': user is not None, 'user': user}
        
        await self.app(scope, receive, send)

    def _is_public_path(self, path: str) -> bool:
        if path == "/api/v1/users/":
            return True
        return any(path.startswith(public_path) for public_path in self.PUBLIC_PATHS)
    
    def _extract_token(self, request: Request) -> Optional[str]:
        return extract_token_from_request(request)
    
    async def _validate_token(self, token: str) -> Optional[models.User]:
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if not email:
                return None
            with SessionLocal() as db:
                return UserCRUD.get_user_by_email(db, email=email)
        except JWTError:
            return None