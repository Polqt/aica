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
    HSTS_MAX_AGE: int = 31536000  
    FORCE_HTTPS: bool = False
    
    DEV_TEST_EMAIL: str = "dev@aica.local"
    DEV_TEST_PASSWORD: str = "DevTest123!"
    DEV_BYPASS_RATE_LIMITING: bool = False
    DEV_MOCK_EXTERNAL_APIS: bool = False

    class Config:
        env_file = str(ENV_FILE_PATH)
        case_sensitive = True
        extra = "ignore"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Security-first environment configuration
        if self.ENVIRONMENT == "production":
            self._configure_production_security()
        elif self.ENVIRONMENT == "staging":
            self._configure_staging_security()
        else:  # development
            self._configure_development_security()
    
    def _configure_production_security(self):
        """Configure security settings for production environment"""
        self.DEBUG = False
        self.SECURE_COOKIES = True
        self.FORCE_HTTPS = True
        self.DOCS_ENABLED = False
        self.REDOC_ENABLED = False
        self.PASSWORD_HASH_ROUNDS = 14
        self.SESSION_TIMEOUT_MINUTES = 60
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 15
        self.DEV_BYPASS_RATE_LIMITING = False
        self.DEV_MOCK_EXTERNAL_APIS = False
        
    def _configure_staging_security(self):
        """Configure security settings for staging environment"""
        self.DEBUG = False
        self.SECURE_COOKIES = True
        self.FORCE_HTTPS = True
        self.DOCS_ENABLED = True
        self.REDOC_ENABLED = True
        self.PASSWORD_HASH_ROUNDS = 12
        self.SESSION_TIMEOUT_MINUTES = 120
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.DEV_BYPASS_RATE_LIMITING = False
        self.DEV_MOCK_EXTERNAL_APIS = False
        
    def _configure_development_security(self):
        """Configure security settings for development environment"""
        self.DEBUG = True
        self.SECURE_COOKIES = False
        self.FORCE_HTTPS = False
        self.DOCS_ENABLED = True
        self.REDOC_ENABLED = True
        self.PASSWORD_HASH_ROUNDS = 8  # Faster for development
        self.SESSION_TIMEOUT_MINUTES = 480
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Longer for development
        # Keep dev settings as configured

settings = Settings()