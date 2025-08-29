from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from .middleware.cors import CORSConfig
from .middleware.security_headers import SecurityHeadersMiddleware
from .middleware.auth import AuthMiddleware
from .v1.routes import auth, users, profiles, matching, jobs

app = FastAPI(
    title="AICA API",
    description="API for AICA application", 
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
cors_config = CORSConfig().get_config()

app.add_middleware(FastAPICORSMiddleware, **cors_config)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthMiddleware)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(profiles.router, prefix="/api/v1", tags=["profile"])
app.include_router(matching.router, prefix="/api/v1/matching", tags=["matching"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])

# Add profile completion status endpoint
from .v1.routes.profiles import get_profile_completion_status
app.add_api_route(
    "/api/v1/profile/completion-status",
    get_profile_completion_status,
    methods=["GET"],
    tags=["profile"]
)

@app.get("/")
async def root():
    return {"message": "AICA API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
