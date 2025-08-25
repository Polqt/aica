from core.config import settings

class CORSConfig:
    def get_config(self):
        return {
            "allow_origins": self._get_allowed_origins(),
            "allow_credentials": True,
            "allow_methods": self._get_allowed_methods(),
            "allow_headers": self._get_allowed_headers(), 
            "expose_headers": self._get_exposed_headers(),
            "max_age": 86400,
        }
    
    def _get_allowed_origins(self):
        """Define allowed origins for CORS based on environment"""
        if settings.ENVIRONMENT == "production":
            # In production, use specific domains
            return settings.ALLOWED_ORIGINS
        else:
            # In development, allow localhost with different ports
            return [
                "http://localhost:3000",
                "http://localhost:3001", 
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                # Add your frontend URL here
                "http://localhost:3000"
            ]
    
    def _get_allowed_methods(self):
        """Define allowed HTTP methods"""
        return ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    
    def _get_allowed_headers(self):
        """Define allowed headers"""
        return [
            "Accept",
            "Accept-Language", 
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token",
            "Cookie",
            "Set-Cookie"
        ]
    
    def _get_exposed_headers(self):
        """Define headers that can be exposed to the browser"""
        return [
            "Content-Type",
            "Authorization",
            "X-Total-Count",
            "X-Page-Count",
            "Set-Cookie"
        ]


# Add separate CORS middleware class for better control
class CORSMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Handle preflight requests
            if scope["method"] == "OPTIONS":
                response = {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [
                        (b"access-control-allow-origin", b"http://localhost:3000"),
                        (b"access-control-allow-methods", b"GET, POST, PUT, DELETE, OPTIONS"),
                        (b"access-control-allow-headers", b"*"),
                        (b"access-control-allow-credentials", b"true"),
                    ],
                }
                await send(response)
                await send({"type": "http.response.body", "body": b""})
                return
        
        await self.app(scope, receive, send)


class OriginValidationMiddleware:
    """Additional origin validation middleware"""
    def __init__(self, app):
        self.app = app
        self.allowed_origins = settings.ALLOWED_ORIGINS
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope["headers"])
            origin = headers.get(b"origin", b"").decode()
            
            # In development, be more permissive
            if settings.ENVIRONMENT == "development":
                if origin.startswith(("http://localhost:", "http://127.0.0.1:")):
                    pass  # Allow localhost origins in development
            elif origin not in self.allowed_origins:
                # In production, strictly validate origins
                response = {
                    "type": "http.response.start",
                    "status": 403,
                    "headers": [(b"content-type", b"text/plain")],
                }
                await send(response)
                await send({
                    "type": "http.response.body", 
                    "body": b"Origin not allowed"
                })
                return
        
        await self.app(scope, receive, send)