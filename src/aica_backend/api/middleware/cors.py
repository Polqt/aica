from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from typing import List
import logging

from ...core.config import settings

logger = logging.getLogger(__name__)

class CORSMiddleware:
    def __init__(self, app):
        self.app = app
        self._configure_cors()
    
    def _configure_cors(self):
        allowed_origins = self._get_allowed_origins()
        
        # Configure CORS middleware
        self.app.add_middleware(
            FastAPICORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,  
            allow_methods=self._get_allowed_methods(),
            allow_headers=self._get_allowed_headers(),
            expose_headers=self._get_exposed_headers(),
            max_age=86400, 
        )
        
        logger.info(f"CORS configured for origins: {allowed_origins}")
    
    def _get_allowed_origins(self) -> List[str]:
        if settings.ENVIRONMENT == "development":
            return [
                "http://localhost:3000",
                "http://localhost:3001", 
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                *settings.ALLOWED_ORIGINS
            ]
        elif settings.ENVIRONMENT == "production":
            return settings.ALLOWED_ORIGINS
        else:
            return settings.ALLOWED_ORIGINS
    
    def _get_allowed_methods(self) -> List[str]:
        return [
            "GET",
            "POST", 
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS" 
        ]
    
    def _get_allowed_headers(self) -> List[str]:
        return [
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "X-Requested-With",
            "X-CSRF-Token", 
            "X-API-Key"    
        ]
    
    def _get_exposed_headers(self) -> List[str]:
        return [
            "X-Total-Count",      
            "X-Rate-Limit-Limit", 
            "X-Rate-Limit-Remaining",
            "X-Rate-Limit-Reset"
        ]

class OriginValidationMiddleware:
    def __init__(self, app):
        self.app = app
        self.trusted_origins = set(settings.ALLOWED_ORIGINS)
        self.suspicious_origins = set()  
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        origin = headers.get(b"origin", b"").decode()
        
        if origin and origin not in self.trusted_origins:
            if settings.ENVIRONMENT == "production":
                logger.warning(f"Untrusted origin attempted access: {origin}")
        
        if origin in self.suspicious_origins:
            logger.error(f"Blocked suspicious origin: {origin}")

        async def send_wrapper(message):
            if message["type"] == "http.response.start" and origin and origin in self.trusted_origins:
                headers = dict(message.get("headers", []))
                headers[b"X-Origin-Verified"] = b"true"
                message["headers"] = list(headers.items())
            await send(message)

        await self.app(scope, receive, send_wrapper)
