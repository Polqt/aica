import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from aica_backend.database.session import SessionLocal
from aica_backend.database.models import JobPosting
from aica_backend.database.repositories.jobs import crud_jobs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DUMMY_JOBS = [
    {
        "job_title": "Senior Full Stack Developer",
        "company_name": "TechCorp Philippines",
        "location": "Makati City, Metro Manila",
        "source_url": "https://dummy.jobsite.com/senior-fullstack-1",
        "source_site": "dummy_site",
        "work_type": "hybrid",
        "employment_type": "full-time",
        "experience_level": "senior",
        "full_text": """
        We are looking for a Senior Full Stack Developer to join our innovative team. 
        
        Requirements:
        - 5+ years of experience in web development
        - Proficient in JavaScript, TypeScript, React, Node.js
        - Experience with Python and Django/FastAPI
        - Strong knowledge of PostgreSQL and database design
        - Familiar with AWS cloud services and Docker
        - Experience with Git version control and CI/CD pipelines
        - Knowledge of modern testing frameworks (Jest, Pytest)
        
        Responsibilities:
        - Design and develop scalable web applications
        - Collaborate with cross-functional teams
        - Mentor junior developers
        - Implement best practices for code quality and security
        - Participate in architecture decisions
        
        Nice to have:
        - Experience with machine learning libraries
        - Knowledge of microservices architecture
        - Familiarity with Kubernetes
        - Mobile development experience
        """,
        "salary_min": 80000,
        "salary_max": 120000,
        "salary_currency": "PHP",
        "salary_period": "monthly"
    },
    {
        "job_title": "Frontend Developer (React)",
        "company_name": "Digital Solutions Inc",
        "location": "Cebu City, Cebu", 
        "source_url": "https://dummy.jobsite.com/frontend-react-2",
        "source_site": "dummy_site",
        "work_type": "remote",
        "employment_type": "full-time", 
        "experience_level": "mid",
        "full_text": """
        Join our dynamic team as a Frontend Developer specializing in React development.
        
        Required Skills:
        - 3+ years of React.js development experience
        - Strong JavaScript and ES6+ knowledge
        - Proficiency in HTML5, CSS3, and responsive design
        - Experience with state management (Redux, Context API)
        - Familiar with modern build tools (Webpack, Vite)
        - Knowledge of RESTful APIs and GraphQL
        - Git version control experience
        
        Responsibilities:
        - Develop user-friendly web interfaces
        - Optimize applications for maximum speed and scalability
        - Collaborate with UX/UI designers
        - Write clean, maintainable code
        - Participate in code reviews
        
        Bonus Skills:
        - TypeScript experience
        - Next.js framework knowledge
        - Testing with Jest and React Testing Library
        - Familiarity with design systems
        """,
        "salary_min": 50000,
        "salary_max": 75000,
        "salary_currency": "PHP",
        "salary_period": "monthly"
    },
    {
        "job_title": "Python Data Scientist",
        "company_name": "Analytics Pro",
        "location": "Bonifacio Global City, Taguig",
        "source_url": "https://dummy.jobsite.com/python-data-scientist-3",
        "source_site": "dummy_site", 
        "work_type": "onsite",
        "employment_type": "full-time",
        "experience_level": "mid",
        "full_text": """
        We're seeking a talented Python Data Scientist to join our analytics team.
        
        Essential Requirements:
        - 3+ years in data science and machine learning
        - Strong Python programming skills (pandas, numpy, scikit-learn)
        - Experience with data visualization (matplotlib, seaborn, plotly)
        - SQL and database querying expertise
        - Statistical analysis and hypothesis testing
        - Machine learning algorithms and model deployment
        - Jupyter notebooks and data exploration
        
        Key Responsibilities:
        - Analyze large datasets to extract business insights
        - Build and deploy machine learning models
        - Create data visualizations and reports
        - Collaborate with business stakeholders
        - Implement data pipelines and automation
        
        Preferred Qualifications:
        - Experience with TensorFlow or PyTorch
        - Cloud platforms (AWS, GCP, Azure)
        - Big data tools (Spark, Hadoop)
        - MLOps and model monitoring
        """,
        "salary_min": 70000,
        "salary_max": 100000,
        "salary_currency": "PHP", 
        "salary_period": "monthly"
    },
    {
        "job_title": "Junior Web Developer",
        "company_name": "StartupHub Manila",
        "location": "Ortigas Center, Pasig",
        "source_url": "https://dummy.jobsite.com/junior-web-dev-4",
        "source_site": "dummy_site",
        "work_type": "hybrid",
        "employment_type": "full-time",
        "experience_level": "entry",
        "full_text": """
        Great opportunity for a Junior Web Developer to grow with our startup team.
        
        Requirements:
        - 1-2 years of web development experience
        - Basic knowledge of HTML, CSS, JavaScript
        - Familiarity with at least one framework (React, Vue, or Angular)
        - Understanding of responsive web design
        - Basic Git knowledge
        - Willingness to learn and adapt quickly
        
        What you'll do:
        - Assist in developing web applications
        - Fix bugs and implement small features
        - Learn from senior developers
        - Participate in team meetings and planning
        - Write documentation
        
        We offer:
        - Mentorship program
        - Learning and development budget
        - Flexible working hours
        - Career growth opportunities
        """,
        "salary_min": 35000,
        "salary_max": 50000,
        "salary_currency": "PHP",
        "salary_period": "monthly"
    },
    {
        "job_title": "DevOps Engineer",
        "company_name": "CloudFirst Solutions",
        "location": "Alabang, Muntinlupa",
        "source_url": "https://dummy.jobsite.com/devops-engineer-5",
        "source_site": "dummy_site",
        "work_type": "onsite", 
        "employment_type": "full-time",
        "experience_level": "senior",
        "full_text": """
        Looking for an experienced DevOps Engineer to streamline our development processes.
        
        Core Requirements:
        - 4+ years of DevOps/Infrastructure experience
        - Strong Linux administration skills
        - Experience with containerization (Docker, Kubernetes)
        - CI/CD pipeline design and implementation
        - Cloud platforms expertise (AWS, Azure, or GCP)
        - Infrastructure as Code (Terraform, CloudFormation)
        - Monitoring and logging tools (Prometheus, ELK stack)
        - Scripting languages (Bash, Python)
        
        Responsibilities:
        - Design and maintain CI/CD pipelines
        - Manage cloud infrastructure and deployments
        - Implement monitoring and alerting systems
        - Optimize system performance and scalability
        - Ensure security best practices
        - Automate repetitive tasks
        
        Advanced Skills:
        - Microservices architecture
        - GitOps workflows
        - Security scanning and compliance
        - Database administration
        """,
        "salary_min": 90000,
        "salary_max": 130000,
        "salary_currency": "PHP",
        "salary_period": "monthly"
    }
]

def create_dummy_jobs():
    db = SessionLocal()
    try:
        logger.info("Creating dummy job postings...")
        
        for job_data in DUMMY_JOBS:
            # Check if job already exists
            existing_job = crud_jobs.get_job_by_source_url(db, job_data["source_url"])
            if existing_job:
                logger.info(f"Job already exists: {job_data['job_title']}")
                continue
                
            # Create new job posting
            job = crud_jobs.create_job_posting(
                db=db,
                url=job_data["source_url"],
                site=job_data["source_site"]
            )
            
            # Update with detailed information
            for key, value in job_data.items():
                if key not in ["source_url", "source_site"]:
                    setattr(job, key, value)
            
            # Set status to processed since we have full data
            job.status = "processed"
            
            db.commit()
            db.refresh(job)
            
            logger.info(f"Created job: {job.job_title} at {job.company_name}")
            
        logger.info("Dummy job creation completed!")
        return True
        
    except Exception as e:
        logger.error(f"Error creating dummy jobs: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = create_dummy_jobs()
    if success:
        print("✅ Dummy jobs created successfully!")
    else:
        print("❌ Failed to create dummy jobs")
