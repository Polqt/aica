from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str
    CRAWL4AI_API_KEY: str
    
    # AI/LLM Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_NAME: str = "llama3:latest"
    OLLAMA_TIMEOUT: int = 120
    
    # Embedding Settings
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    VECTOR_SIMILARITY_THRESHOLD: float = 0.75
    
    # Pipeline Settings
    SCRAPING_BATCH_SIZE: int = 100
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 60
    PIPELINE_TIMEOUT: int = 3600
    
    JOB_SITES_CONFIG: dict = {
        ""
    }
    
    # Monitoring & Logging
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    ALERT_WEBHOOK_URL: str = ""
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    ENVIRONMENT: str = "development"
    SECURE_COOKIES: bool = False
    RATE_LIMIT_PER_MINUTE: int = 60
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    JOB_SITES_CONFIG: dict = {
        "jobstreet": {
            "base_url": "https://ph.jobstreet.com/",
            "search_urls": [
                "/jobs-",
                "",
                "",
                "",
            ],
            "selectors": {
                "job_links": "a[data-automation='jobTitle']",
                "job_title": "h1[data-automation='job-detail-title']",
                "company": "span[data-automation='advertiser-name']",
                "description": "div[data-automation='job-description']",
            },
            "rate_limit": 100,
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        }
    }

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
