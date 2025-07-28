from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .v1.endpoints import profiles, users, login, jobs
from ..core.config import settings

# Rate limiting imports
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    
    # Create rate limiter
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=settings.REDIS_URL.replace("/0", "/1")  # Use different Redis DB for rate limiting
    )
    RATE_LIMITING_ENABLED = True
except ImportError:
    print("⚠️  slowapi not installed. Rate limiting disabled. Install with: pip install slowapi")
    limiter = None
    RATE_LIMITING_ENABLED = False

app = FastAPI(
    title="AICA Backend",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Add rate limiting to app
if RATE_LIMITING_ENABLED:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "Accept",
        "Origin",
    ],
    expose_headers=["X-Total-Count"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(login.router, prefix="/api/v1", tags=["Login"])
app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["Profiles"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])

@app.get("/health", tags=['Status'])
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }