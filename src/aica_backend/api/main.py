from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from .v1.routes import auth, profiles, users, jobs, matching  
from .middleware import (
    SecurityHeadersMiddleware, 
    RequestSanitizationMiddleware,
    OriginValidationMiddleware
)
from ..core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    
    # Temporarily disable Redis rate limiting for local development
    # limiter = Limiter(
    #     key_func=get_remote_address,
    #     storage_uri=settings.REDIS_URL.replace("/0", "/1"),  #
    # )
    # RATE_LIMITING_ENABLED = True
    # logger.info("Rate limiting enabled with Redis backend")
    
    # For now, disable rate limiting
    limiter = None
    RATE_LIMITING_ENABLED = False
    logger.info("Rate limiting disabled for local development")
except ImportError:
    logger.warning("slowapi not installed. Rate limiting disabled. Install with: pip install slowapi")
    limiter = None
    RATE_LIMITING_ENABLED = False
except Exception as e:
    logger.error(f"Rate limiting setup failed: {str(e)}")
    limiter = None
    RATE_LIMITING_ENABLED = False

app = FastAPI(
    title="AICA Backend API",
    description="AI Career Assistant - Intelligent Job Matching and Resume Building Platform",
    version="1.0.0",
    docs_url="/docs" if settings.DOCS_ENABLED else None,
    redoc_url="/redoc" if settings.REDOC_ENABLED else None,
    openapi_url="/openapi.json" if settings.DOCS_ENABLED else None,
    servers=[
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://api.aica.com", "description": "Production server"}
    ] if settings.ENVIRONMENT == "production" else None
)

if RATE_LIMITING_ENABLED:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(RequestSanitizationMiddleware)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(OriginValidationMiddleware)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=[
        "localhost", 
        "127.0.0.1", 
        "0.0.0.0",
        *settings.ALLOWED_HOSTS
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "Accept",
        "Origin",
        "X-CSRF-Token",
        "X-API-Key"
    ],
    expose_headers=[
        "X-Total-Count",
        "X-Rate-Limit-Limit",
        "X-Rate-Limit-Remaining",
        "X-Rate-Limit-Reset"
    ],
    max_age=86400,
)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    import time
    
    start_time = time.time()
    
    logger.info(
        f"REQUEST: {request.method} {request.url.path} | "
        f"IP: {request.client.host if request.client else 'unknown'} | "
        f"User-Agent: {request.headers.get('User-Agent', 'unknown')[:100]}"
    )
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response info
    logger.info(
        f"RESPONSE: {response.status_code} | "
        f"Time: {process_time:.4f}s | "
        f"Path: {request.url.path}"
    )
    
    return response

# API Routes
app.include_router(
    auth.router, 
    prefix="/api/v1", 
    tags=["Authentication"],
    responses={
        401: {"description": "Unauthorized"},
        429: {"description": "Too Many Requests"}
    }
)

app.include_router(
    users.router, 
    prefix="/api/v1/users", 
    tags=["Users"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"}
    }
)

app.include_router(
    profiles.router, 
    prefix="/api/v1/profiles", 
    tags=["Profiles"],
    dependencies=[], 
    responses={
        401: {"description": "Unauthorized"}
    }
)

app.include_router(
    jobs.router, 
    prefix="/api/v1/jobs", 
    tags=["Jobs"],
    responses={
        401: {"description": "Unauthorized"}
    }
)

app.include_router(
    matching.router,
    prefix="/api/v1/matching",
    tags=["Job Matching"],
    responses={
        401: {"description": "Unauthorized"}
    }
)

# app.include_router(
#     scraping.router,
#     prefix="/api/v1/scraping",
#     tags=["Scraping Management"],
#     responses={
#         401: {"description": "Unauthorized"}
#     }
# )

# app.include_router(
#     pipeline.router,
#     prefix="/api/v1/pipeline",
#     tags=["Pipeline Management"],
#     responses={
#         401: {"description": "Unauthorized"}
#     }
# )