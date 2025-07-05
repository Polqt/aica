from fastapi import FastAPI
from .v1.endpoints import profiles

app = FastAPI(title="AICA Backend")

app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["Profiles"])

@app.get("/health", tags=['Status'])

def health_check():
    return {
        "status": "ok"
    }