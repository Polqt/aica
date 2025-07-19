from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str
    CRAWL4AI_API_KEY: str
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    ENVIRONMENT: str = "development"
    SECURE_COOKIES: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
