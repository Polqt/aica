from ...core.config import settings

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
            return settings.ALLOWED_ORIGINS
        else:
            return list(set([
                "http://localhost:3000",
                "http://localhost:3001",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
            ]))

    def _get_allowed_methods(self):
        return ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]

    def _get_allowed_headers(self):
        return [
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token",
            "Cookie",
            "Set-Cookie",
        ]

    def _get_exposed_headers(self):
        return [
            "Content-Type",
            "Authorization",
            "X-Total-Count",
            "X-Page-Count",
            "Set-Cookie",
        ]


class OriginValidationMiddleware:
    """Additional origin validation middleware"""
    def __init__(self, app):
        self.app = app
        self.allowed_origins = settings.ALLOWED_ORIGINS

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope["headers"])
            origin = headers.get(b"origin", b"").decode()

            if settings.ENVIRONMENT == "development":
                if origin.startswith(("http://localhost:", "http://127.0.0.1:")):
                    pass  # Allow localhost origins in dev
            elif origin not in self.allowed_origins:
                response = {
                    "type": "http.response.start",
                    "status": 403,
                    "headers": [(b"content-type", b"text/plain")],
                }
                await send(response)
                await send({
                    "type": "http.response.body",
                    "body": b"Origin not allowed",
                })
                return

        await self.app(scope, receive, send)
