from fastapi import FastAPI

app = FastAPI(title="AICA Backend")

@app.get("/health", tags=['Status'])

def health_check():
    return {
        "status": "ok"
    }