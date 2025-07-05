from fastapi import FastAPI
from .v1.endpoints import profiles, users, login

app = FastAPI(title="AICA Backend")

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(login.router, prefix="/api/v1", tags=["Login"])
app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["Profiles"])

@app.get("/health", tags=['Status'])

def health_check():
    return {
        "status": "ok"
    }