from typing import List
from pydantic_settings import BaseSettings
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    
    # Authentication & Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password Security
    PASSWORD_HASH_ROUNDS: int = 12
    
    # Redis Configuration
    REDIS_URL: str
    
    # External APIs
    CRAWL4AI_API_KEY: str
    
    # AI/LLM Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_NAME: str = "llama3:latest"
    OLLAMA_TIMEOUT: int = 120
    
    # Embedding Settings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    VECTOR_SIMILARITY_THRESHOLD: float = 0.75
    VECTOR_BACKEND: str = "pgvector"  # Options: pgvector, faiss
    
    # Scraping Configuration (ADDED MISSING FIELDS)
    SCRAPING_ENABLED: bool = True
    SCRAPING_RATE_LIMIT_DELAY: int = 2
    SCRAPING_MAX_RETRIES: int = 3
    SCRAPING_TIMEOUT: int = 120
    
    # Crawl4AI Configuration (ADDED MISSING FIELDS)
    CRAWL4AI_HEADLESS: bool = False
    CRAWL4AI_BROWSER_TYPE: str = "chromium"
    CRAWL4AI_USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
    
    # Pipeline Settings
    SCRAPING_BATCH_SIZE: int = 100
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 60
    PIPELINE_TIMEOUT: int = 3600
    
    # Basic Configuration
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = str(PROJECT_ROOT / ".env")
        case_sensitive = True
        extra = "ignore"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]


settings = Settings()