from typing import Dict
import logging


from ...core.config import settings

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware:
    
    def __init__(self, app):
        self.app = app
        self.security_headers = self._get_security_headers()
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                for header_name, header_value in self.security_headers.items():
                    headers[header_name.encode()] = header_value.encode()
                message["headers"] = list(headers.items())
            await send(message)

        await self.app(scope, receive, send_wrapper)
    
    def _get_security_headers(self) -> Dict[str, str]:
        base_headers = {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            
            # Prevent clickjacking attacks - Changed from DENY to SAMEORIGIN for dev
            "X-Frame-Options": "SAMEORIGIN" if settings.ENVIRONMENT != "production" else "DENY",
            
            # Enable XSS protection in browsers
            "X-XSS-Protection": "1; mode=block",
            
            # Control referrer information
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Prevent DNS prefetching
            "X-DNS-Prefetch-Control": "off",
            
            # Disable Adobe Flash and PDF plugins
            "X-Permitted-Cross-Domain-Policies": "none",
        }
        
        if settings.ENVIRONMENT == "production":
            base_headers.update({
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
                "Content-Security-Policy": self._get_csp_policy(),
            })
        else:
            base_headers["Content-Security-Policy"] = (
                "default-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "connect-src 'self' http://localhost:3000 http://localhost:8000 ws://localhost:3000; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https: http:; "
                "font-src 'self' data:; "
            )
        
        return base_headers
    
    def _get_csp_policy(self) -> str:
        if settings.ENVIRONMENT == "production":
            return (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )
        else:
            return (
                "default-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "connect-src 'self' http://localhost:3000 http://localhost:8000 ws://localhost:3000; "
                "img-src 'self' data: https: http:"
            )

class RequestSanitizationMiddleware:
    def __init__(self, app):
        self.app = app
        self.suspicious_patterns = [
            "<script", "javascript:", "vbscript:", "onload=", "onerror=",
            "eval(", "expression(", "url(", "import(", "__import__",
            "SELECT * FROM", "DROP TABLE", "INSERT INTO", "DELETE FROM",
            "../", "..\\", "/etc/passwd", "/etc/shadow", "cmd.exe", "powershell"
        ]
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if self._contains_suspicious_content(path):
            logger.warning(f"Suspicious request path detected: {path}")
            response = {
                "type": "http.response.start",
                "status": 400,
                "headers": [(b"content-type", b"text/plain")],
            }
            await send(response)
            await send({
                "type": "http.response.body",
                "body": b"Bad Request: Suspicious content detected",
            })
            return

        await self.app(scope, receive, send)
    
    def _contains_suspicious_content(self, content: str) -> bool:
        content_lower = content.lower()
        return any(pattern.lower() in content_lower for pattern in self.suspicious_patterns)