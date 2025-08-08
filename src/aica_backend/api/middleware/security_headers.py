from fastapi import Request, Response
from typing import Dict, Any
import logging

from ...core.config import settings

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware:
    
    def __init__(self):
        self.security_headers = self._get_security_headers()
    
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        
        for header_name, header_value in self.security_headers.items():
            response.headers[header_name] = header_value
        
        if settings.ENVIRONMENT == "development":
            logger.debug(f"Applied security headers to {request.url.path}")
        
        return response
    
    def _get_security_headers(self) -> Dict[str, str]:
        base_headers = {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            
            # Prevent clickjacking attacks
            "X-Frame-Options": "DENY",
            
            # Enable XSS protection in browsers
            "X-XSS-Protection": "1; mode=block",
            
            # Control referrer information
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Prevent DNS prefetching
            "X-DNS-Prefetch-Control": "off",
            
            # Disable Adobe Flash and PDF plugins
            "X-Permitted-Cross-Domain-Policies": "none",
        }
        
        # Add HSTS only in production with HTTPS
        if settings.ENVIRONMENT == "production":
            base_headers.update({
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
                "Content-Security-Policy": self._get_csp_policy(),
            })
        else:
            # Relaxed CSP for development
            base_headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'"
        
        return base_headers
    
    def _get_csp_policy(self) -> str:
        if settings.ENVIRONMENT == "production":
            return (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )
        else:
            return "default-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:"

class RequestSanitizationMiddleware:
    def __init__(self):
        self.suspicious_patterns = [
            "<script", "javascript:", "vbscript:", "onload=", "onerror=",
            "eval(", "expression(", "url(", "import(", "__import__",
            "SELECT * FROM", "DROP TABLE", "INSERT INTO", "DELETE FROM",
            "../", "..\\", "/etc/passwd", "/etc/shadow", "cmd.exe", "powershell"
        ]
    
    async def __call__(self, request: Request, call_next):
        try:
            if self._contains_suspicious_content(request.url.path):
                logger.warning(f"Suspicious request path detected: {request.url.path}")
                return Response(
                    content="Bad Request: Suspicious content detected",
                    status_code=400
                )
            
            user_agent = request.headers.get("User-Agent", "")
            if not user_agent or len(user_agent) > 500:
                logger.warning(f"Suspicious User-Agent: {user_agent[:100]}...")
            
            return await call_next(request)
            
        except Exception as e:
            logger.error(f"Request sanitization error: {str(e)}")
            return await call_next(request)
    
    def _contains_suspicious_content(self, content: str) -> bool:
        content_lower = content.lower()
        return any(pattern.lower() in content_lower for pattern in self.suspicious_patterns)
