from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from .middleware.cors import CORSConfig
from .middleware.security_headers import SecurityHeadersMiddleware
from .middleware.auth import AuthMiddleware
from .v1.routes import auth, users

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

@app.get("/")
async def root():
    return {"message": "AICA API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}