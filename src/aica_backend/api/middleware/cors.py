from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging

from ...core.config import settings

logger = logging.getLogger(__name__)

class EnhancedCORSMiddleware:
    def __init__(self, app):
        self.app = app
        self._configure_cors()
    
    def _configure_cors(self):
        allowed_origins = self._get_allowed_origins()
        
        # Configure CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
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
            "X-CSRF-Token",  # For future CSRF protection
            "X-API-Key"      # For future API key authentication
        ]
    
    def _get_exposed_headers(self) -> List[str]:
        return [
            "X-Total-Count",      # For pagination
            "X-Rate-Limit-Limit", # For rate limiting info
            "X-Rate-Limit-Remaining",
            "X-Rate-Limit-Reset"
        ]

class OriginValidationMiddleware:
    def __init__(self):
        self.trusted_origins = set(settings.ALLOWED_ORIGINS)
        self.suspicious_origins = set()  
    
    async def __call__(self, request: Request, call_next):
        origin = request.headers.get("Origin")
        referer = request.headers.get("Referer")
        
        if origin and origin not in self.trusted_origins:
            if settings.ENVIRONMENT == "production":
                logger.warning(f"Untrusted origin attempted access: {origin}")
        
        if origin in self.suspicious_origins:
            logger.error(f"Blocked suspicious origin: {origin}")
        
        response = await call_next(request)
        
        if origin and origin in self.trusted_origins:
            response.headers["X-Origin-Verified"] = "true"
        
        return response
