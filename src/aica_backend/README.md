# AICA Backend - AI Career Assistant

A modular, AI-powered backend system for ethical job scraping, intelligent matching, and resume building.

## 🏗️ Architecture Overview

The AICA Backend follows a clean, modular architecture with clear separation of concerns:

```
src/aica_backend/
├── api/                    # FastAPI application layer
│   ├── v1/endpoints/      # API endpoints (auth, jobs, matching, resume, pipeline)
│   ├── v1/schemas/        # Pydantic models for API validation
│   ├── middleware/        # Custom middleware (CORS, security, rate limiting)
│   └── dependencies.py   # Dependency injection
├── services/              # Business logic layer (NEW)
│   ├── scraping/         # Job scraping services
│   ├── ai/               # AI/ML services (skill extraction, RAG, matching)
│   ├── profile_service.py # Profile management
│   ├── resume_service.py  # Resume building
│   └── pipeline_service.py # Complete pipeline orchestration
├── db/                    # Database layer
│   ├── models.py         # SQLAlchemy models
│   ├── session.py        # Database connection
│   └── base_class.py     # Base model class
├── crud/                  # Data access layer
├── core/                  # Configuration and utilities
├── workers/               # Celery background tasks
│   └── tasks/            # Task definitions
└── main.py               # Application entry point
```

## ✨ Key Features

### 🔍 Ethical Job Scraping
- **Rate-limited scraping** from approved sources (JobStreet Philippines)
- **Structured data extraction** using BeautifulSoup and custom selectors
- **Content cleaning and validation**
- **Duplicate detection** and deduplication

### 🤖 AI-Powered Skills Matching
- **Local NLP processing** using Sentence Transformers (no paid APIs)
- **Skill extraction** from job descriptions using pattern matching
- **Vector embeddings** for semantic similarity search
- **Job-profile matching** with similarity scoring

### 📄 Resume Builder
- **Multiple templates** (Modern, Classic, Creative, Minimal)
- **AI-powered suggestions** for resume improvement
- **Job-specific optimization** with skill gap analysis
- **Multiple export formats** (JSON, TXT, HTML)

### 🔄 RAG Pipeline
- **Job explanations** with contextual insights
- **Skill gap analysis** with learning recommendations
- **Career advice** generation
- **Similar job discovery**

### 📊 Pipeline Management
- **Complete workflow orchestration** from scraping to matching
- **Background processing** with Celery
- **Progress tracking** and error handling
- **Performance metrics** and analytics

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

## 🔧 Service Layer Architecture

### ScrapingService
```python
from services import ScrapingService

service = ScrapingService()

# Scrape jobs from a site
jobs = await service.scrape_site("jobstreet", extract_details=True, max_jobs=10)

# Extract content from a specific URL
content = await service.extract_job_content("https://...")
```

### JobMatchingService
```python
from services import JobMatchingService

matching_service = JobMatchingService()

# Get job recommendations for a user
recommendations = matching_service.get_job_recommendations(
    user_id=1, db=db, limit=10
)

# Find similar jobs
matches = matching_service.find_matching_jobs(profile, db)
```

### RAGService
```python
from services import RAGService

rag_service = RAGService()

# Explain a job posting
explanation = rag_service.explain_job_posting(job, user_profile)

# Analyze skill gaps
analysis = rag_service.analyze_skill_gap(job, profile)

# Generate career advice
advice = rag_service.generate_career_advice(job, profile)
```

### PipelineService
```python
from services import PipelineService

pipeline = PipelineService()

# Run complete pipeline
result = await pipeline.run_full_pipeline(db, site_names=["jobstreet"])

# Get pipeline status
status = pipeline.get_pipeline_status(db)

# Get performance metrics
metrics = pipeline.get_pipeline_metrics(db, days=30)
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