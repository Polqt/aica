# AICA Backend - AI Career Assistant

A modular, AI-powered backend system for ethical job scraping, intelligent matching, and resume building. Refactored following YAGNI, KISS, DRY, and CLEAN CODE principles for optimal maintainability and performance.

## 🏗️ Architecture Overview

The AICA Backend follows a clean, modular architecture with clear separation of concerns:

```
src/aica_backend/
├── ai/                    # Modular AI components (NEW)
│   ├── skill_extraction.py # Skill extraction from job descriptions
│   ├── job_matching.py    # AI-powered job matching algorithms
│   ├── embeddings.py      # Embedding operations interface
│   └── generation.py      # Text generation services
├── api/                   # FastAPI application layer
│   ├── v1/endpoints/      # API endpoints (auth, jobs, matching, resume, pipeline)
│   ├── v1/schemas/        # Pydantic models for API validation
│   ├── middleware/        # Custom middleware (CORS, security, rate limiting)
│   └── dependencies.py    # Dependency injection
├── core/                  # Configuration and utilities
├── database/              # Database layer
│   ├── models/           # SQLAlchemy models
│   ├── repositories/     # Data access layer
│   ├── session.py        # Database connection
│   └── base_class.py     # Base model class
├── rag/                   # Retrieval-Augmented Generation
│   ├── embeddings/       # Vector embeddings and storage
│   ├── generation/       # LLM text generation
│   └── pipeline/         # RAG orchestration pipeline
├── scraping/              # Ethical web scraping
│   ├── providers/        # Scraping provider implementations
│   └── config.py         # Scraping configuration
├── services/              # Business logic layer
│   ├── scraping_service.py      # Job scraping orchestration
│   └── job_matching_service.py  # Job matching business logic
├── utils/                 # Consolidated utilities
│   ├── common.py         # Common utility functions (DRY)
│   ├── rate_limiter.py   # Simple rate limiting
│   └── robots_checker.py # Robots.txt compliance
└── main.py               # Application entry point
```

## ✨ Key Features

### 🔍 Ethical Job Scraping
- **Dual scraping providers**: BeautifulSoup (lightweight) and Crawl4AI (advanced)
- **Rate-limited scraping** with robots.txt compliance
- **Structured data extraction** with fallback mechanisms
- **Content cleaning and validation** with duplicate detection

### 🤖 AI-Powered Skills Matching
- **Modular AI components** with clear separation of concerns
- **Hybrid skill extraction**: Pattern matching + LLM-based extraction
- **Optimized pgvector integration** with performance indexes
- **Advanced similarity algorithms** with multiple scoring methods

### 📄 Resume Builder
- **Multiple templates** (Modern, Classic, Creative, Minimal)
- **AI-powered suggestions** for resume improvement
- **Job-specific optimization** with skill gap analysis
- **Multiple export formats** (JSON, TXT, HTML)

### 🔄 Enhanced RAG Pipeline
- **LangChain integration** for better orchestration
- **Modular pipeline components** for scalability
- **Contextual job explanations** with AI insights
- **Intelligent skill gap analysis** and recommendations

### 📊 Improved Pipeline Management
- **Streamlined workflow orchestration** following KISS principles
- **Consistent error handling** across all services
- **Performance monitoring** with health checks
- **Batch processing capabilities** for efficiency

## 🔧 Refactoring & Best Practices Applied

This codebase has been refactored following software engineering best practices:

### ✅ YAGNI (You Aren't Gonna Need It)
- Removed over-engineered features like complex circuit breakers and extensive metrics
- Simplified configuration by removing unused settings
- Streamlined dependencies to only what's necessary

### ✅ KISS (Keep It Simple, Stupid)
- Simplified base provider from 265 lines to 35 lines
- Created simple, focused utility functions
- Reduced configuration complexity

### ✅ DRY (Don't Repeat Yourself)
- Consolidated duplicate utility functions into `utils/common.py`
- Created reusable error handling patterns
- Unified response formatting across services

### ✅ CLEAN CODE Principles
- Clear separation of concerns with modular AI components
- Consistent error handling and response formatting
- Meaningful naming and comprehensive documentation
- Single responsibility principle applied throughout

### 🚀 Performance Optimizations
- Optimized pgvector integration with connection pooling
- Added batch processing capabilities
- Created performance indexes for vector similarity search
- Improved async/await patterns throughout

### 🔒 Ethical & Zero-Cost Approach
- Maintained ethical scraping practices with robots.txt compliance
- Used only free, open-source tools (Sentence Transformers, pgvector, LangChain)
- No paid API dependencies for core functionality

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/aica_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=localhost
POSTGRES_DB=aica_db
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# AI/ML Settings
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
VECTOR_SIMILARITY_THRESHOLD=0.75

# External APIs
CRAWL4AI_API_KEY=your-crawl4ai-key
```

### 3. Database Setup

```bash
# Run migrations (if using Alembic)
alembic upgrade head
```

### 4. Start the Application

```bash
# Development server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start Background Workers

```bash
# Start Celery worker
celery -A workers.celery_app worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A workers.celery_app beat --loglevel=info
```

## 📚 API Documentation

Once running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Modular Architecture

### AI Components
```python
from ai import skill_extraction_service, job_matching_ai_service, generation_service

# Extract skills from job description
skills = await skill_extraction_service.extract_skills_from_job(job_description)

# Calculate match score
score = await job_matching_ai_service.calculate_match_score(user_skills, job_skills)

# Generate career advice
advice = await generation_service.generate_career_advice(user_profile, matches)
```

### Service Layer
```python
from services.scraping_service import ScrapingService
from services.job_matching_service import JobMatchingService

# Scraping with dual providers
scraping_service = ScrapingService()
jobs = await scraping_service.start_scraping_pipeline(urls)

# Job matching with RAG
matching_service = JobMatchingService()
matches = await matching_service.find_job_matches(user_id, db)
```

### RAG Pipeline
```python
from rag.pipeline.rag_pipeline import rag_pipeline

# Enhanced RAG with LangChain integration
matches = await rag_pipeline.find_matching_jobs(
    session=db,
    user_id=user_id,
    user_skills=user_skills,
    generate_explanation=True
)

# Extract skills using LangChain
skills = await rag_pipeline.extract_job_skills_langchain(job_description)
```

### Vector Store
```python
from rag.embeddings.vector_store import vector_store

# Optimized pgvector operations
await vector_store.store_job_embeddings_batch(session, job_embeddings)
await vector_store.create_performance_indexes(session)
health = await vector_store.health_check()
```

## 🎯 API Endpoints

### Authentication
- `POST /api/v1/login/access-token` - Login
- `POST /api/v1/users/` - Register
- `GET /api/v1/users/me` - Get current user

### Profile Management
- `GET /api/v1/profiles/profile` - Get user profile
- `PUT /api/v1/profiles/profile` - Update profile

### Job Matching
- `GET /api/v1/matching/recommendations` - Get job recommendations
- `GET /api/v1/matching/jobs/{job_id}/similar` - Get similar jobs
- `GET /api/v1/matching/jobs/{job_id}/match-analysis` - Analyze job match
- `POST /api/v1/matching/jobs/bulk-match` - Bulk job matching

### Resume Builder
- `POST /api/v1/resume/generate` - Generate resume
- `GET /api/v1/resume/suggestions` - Get improvement suggestions
- `POST /api/v1/resume/optimize-for-job/{job_id}` - Optimize for specific job
- `POST /api/v1/resume/export` - Export resume

### Pipeline Management
- `GET /api/v1/pipeline/status` - Get pipeline status
- `POST /api/v1/pipeline/trigger` - Trigger manual pipeline
- `GET /api/v1/pipeline/metrics` - Get performance metrics
- `GET /api/v1/pipeline/history` - Get execution history

## 🛡️ Security Features

- **JWT Authentication** with httpOnly cookies
- **Rate limiting** with Redis backend
- **Request validation** with Pydantic schemas
- **CORS protection** with origin validation
- **Security headers** middleware
- **Input sanitization** for XSS prevention

## 📈 Performance & Scalability

- **Async/await** throughout for non-blocking operations
- **Connection pooling** for database efficiency
- **Background task processing** with Celery
- **Vector similarity search** with pgVector
- **Local AI models** for zero-cost inference
- **Efficient data models** with SQLAlchemy 2.0

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest tests/

# Test scraping service
python test_scraping.py
```

## 🔄 Development Workflow

1. **Services-First Development**: Implement business logic in services
2. **API Layer**: Create endpoints that use services
3. **Background Tasks**: Use services in Celery tasks
4. **Testing**: Test services independently of API
5. **Documentation**: Update API schemas and docs

## 📊 Monitoring & Metrics

- **Pipeline execution tracking** with detailed metrics
- **Error logging** and retry mechanisms
- **Performance analytics** for scraping and matching
- **Database query optimization**

## 🚀 Deployment

The backend is containerized and ready for deployment:

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Follow **DRY and SOLID principles**
2. **Services contain business logic**, APIs handle HTTP concerns
3. **Test services independently** before API integration
4. **Use type hints** and Pydantic models for validation
5. **Log appropriately** with structured logging

## 📝 Notes

- **Zero-cost approach**: Uses only free, open-source tools
- **Ethical scraping**: Respects rate limits and robots.txt
- **Local AI processing**: No external API dependencies for core features
- **Modular design**: Easy to extend and maintain
- **Production-ready**: Includes security, monitoring, and scalability features

This restructured backend provides a solid foundation for AI-powered career assistance while maintaining simplicity, performance, and ethical practices.