from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from .middleware.cors import CORSConfig

app = FastAPI(...)

cors_config = CORSConfig().get_config()
app.add_middleware(FastAPICORSMiddleware, **cors_config)
