from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .v1.endpoints import profiles, users, login, jobs
from ..core.config import settings

app = FastAPI(
    title="AICA Backend",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
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