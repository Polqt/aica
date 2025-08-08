from typing import List
from pydantic_settings import BaseSettings

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
    MIN_PASSWORD_LENGTH: int = 8
    MAX_PASSWORD_LENGTH: int = 128
    REQUIRE_SPECIAL_CHARS: bool = True
    PASSWORD_HASH_ROUNDS: int = 12
    
    # Session Security
    SESSION_TIMEOUT_MINUTES: int = 480  
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
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
    
    # Pipeline Settings
    SCRAPING_BATCH_SIZE: int = 100
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 60
    PIPELINE_TIMEOUT: int = 3600
    
    # Job Scraping Configuration
    JOB_SITES_CONFIG: dict = {
        # "jobstreet": {
        #     "base_url": "https://www.jobstreet.com.ph/",
        #     "search_urls": [
        #         "/en/job-search/software-developer-jobs",
        #         "/en/job-search/python-developer-jobs", 
        #         "/en/job-search/web-developer-jobs",
        #         "/en/job-search/data-scientist-jobs",
        #         "/en/job-search/software-engineer-jobs",
        #         "/en/job-search/frontend-developer-jobs",
        #         "/en/job-search/backend-developer-jobs",
        #         "/en/job-search/full-stack-developer-jobs",
        #         "/en/job-search/mobile-developer-jobs",
        #         "/en/job-search/devops-engineer-jobs"
        #     ],
        #     "selectors": {
        #         "job_links": "h3 a[href*='/job/']",
        #         "job_title": "h1[data-automation='job-detail-title']",
        #         "company": "span[data-automation='advertiser-name']",
        #         "description": "div[data-automation='job-description']",
        #         "location": "span[data-automation='job-detail-location']",
        #         "salary": "span[data-automation='job-detail-salary']",
        #         "work_type": "span[data-automation='job-detail-work-type']",
        #         "employment_type": "span[data-automation='job-detail-employment-type']",
        #         "posting_date": "span[data-automation='job-detail-date']",
        #         "benefits": "span[data-automation='job-detail-benefits']"
        #     },
        #     "rate_limit": 20,
        #     "headers": {
        #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        #     }
        # },
    }
    
    # Security & Monitoring
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    ALERT_WEBHOOK_URL: str = ""
    ENABLE_AUDIT_LOG: bool = True
    
    # Rate Limiting & DDoS Protection
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    BURST_RATE_LIMIT: int = 100
    
    # File Upload Security
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    UPLOAD_SCAN_ENABLED: bool = True
    
    # CORS & Headers
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Environment Configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECURE_COOKIES: bool = False
    
    # API Documentation
    DOCS_ENABLED: bool = True
    REDOC_ENABLED: bool = True
    
    # Content Security Policy
    CSP_POLICY: str = "default-src 'self'"
    
    # Additional Security Headers
    HSTS_MAX_AGE: int = 31536000  # 1 year
    FORCE_HTTPS: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-configure based on environment
        if self.ENVIRONMENT == "production":
            self.DEBUG = False
            self.DOCS_ENABLED = False
            self.REDOC_ENABLED = False
            self.SECURE_COOKIES = True
            self.FORCE_HTTPS = True
        elif self.ENVIRONMENT == "development":
            self.DEBUG = True
            self.DOCS_ENABLED = True
            self.REDOC_ENABLED = True
            self.SECURE_COOKIES = False
            self.FORCE_HTTPS = False

settings = Settings()
