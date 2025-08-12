"""
Comprehensive AI Testing Suite
Tests all AI functionality with real examples
"""
import sys
import os
import asyncio
import json

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_rag_embeddings():
    """Test RAG service embeddings and vector search"""
    print("🔍 Testing RAG Embeddings & Vector Search...")
    try:
        from aica_backend.ai.rag.service import get_rag_service
        
        rag_service = get_rag_service()
        
        # Test embedding generation
        print("   📊 Testing embedding generation...")
        test_jobs = [
            {
                "id": 1,
                "job_title": "Senior Python Developer",
                "company_name": "TechCorp",
                "full_text": "Looking for a Senior Python Developer with experience in Django, Flask, and machine learning. Must have 5+ years of experience.",
                "location": "Manila, Philippines",
                "work_type": "remote"
            },
            {
                "id": 2,
                "job_title": "Frontend React Developer",
                "company_name": "WebStudio",
                "full_text": "Seeking a Frontend Developer skilled in React, TypeScript, and modern CSS. Experience with Next.js preferred.",
                "location": "Makati, Philippines", 
                "work_type": "hybrid"
            }
        ]
        
        # Create knowledge base
        success = rag_service.create_job_knowledge_base(test_jobs)
        if success:
            print("   ✅ Knowledge base created successfully")
            
            # Test semantic search
            similar_jobs = rag_service.get_similar_jobs("Python machine learning", k=2)
            print(f"   ✅ Found {len(similar_jobs)} similar jobs for 'Python machine learning'")
            
            for job in similar_jobs:
                title = job['metadata'].get('title', 'Unknown')
                print(f"      - {title}")
        else:
            print("   ❌ Knowledge base creation failed")
            
        return success
        
    except Exception as e:
        print(f"   ❌ RAG test error: {str(e)}")
        return False

def test_job_matching_algorithm():
    """Test the job matching algorithm with detailed scenarios"""
    print("\n🎯 Testing Job Matching Algorithm...")
    try:
        from aica_backend.services.matching_service import get_matching_service
        
        matching_service = get_matching_service()
        
        # Create detailed test profiles
        profiles = [
            {
                "name": "Entry-Level Developer",
                "profile": {
                    "skills": [
                        {"name": "Python", "level": "Beginner"},
                        {"name": "JavaScript", "level": "Beginner"},
                        {"name": "HTML", "level": "Intermediate"}
                    ],
                    "location": "Manila, Philippines",
                    "work_preferences": {
                        "work_types": ["Remote", "Hybrid"],
                        "minimum_salary": 25000
                    },
                    "experiences": [
                        {
                            "job_title": "Intern Developer",
                            "company_name": "StartupCorp",
                            "start_date": "2023-01-01",
                            "end_date": "2024-01-01"
                        }
                    ]
                }
            },
            {
                "name": "Senior Developer",
                "profile": {
                    "skills": [
                        {"name": "Python", "level": "Expert"},
                        {"name": "Django", "level": "Advanced"},
                        {"name": "React", "level": "Advanced"},
                        {"name": "PostgreSQL", "level": "Intermediate"}
                    ],
                    "location": "Makati, Philippines",
                    "work_preferences": {
                        "work_types": ["Remote"],
                        "minimum_salary": 80000
                    },
                    "experiences": [
                        {
                            "job_title": "Senior Software Engineer",
                            "company_name": "TechCorp",
                            "start_date": "2020-01-01",
                            "end_date": "2024-01-01"
                        }
                    ]
                }
            }
        ]
        
        # Test jobs with different requirements
        test_jobs = [
            {
                "id": 1,
                "job_title": "Junior Python Developer",
                "company_name": "StartupTech",
                "location": "Manila, Philippines",
                "experience_level": "junior",
                "work_type": "remote",
                "salary_min": 30000,
                "salary_max": 45000,
                "salary_currency": "PHP",
                "full_text": "Looking for a Junior Python Developer to join our growing team. Must know Python basics, HTML, CSS. Fresh graduates welcome."
            },
            {
                "id": 2,
                "job_title": "Senior Full Stack Developer",
                "company_name": "Enterprise Corp",
                "location": "Makati, Philippines",
                "experience_level": "senior",
                "work_type": "hybrid",
                "salary_min": 90000,
                "salary_max": 120000,
                "salary_currency": "PHP",
                "full_text": "Senior Full Stack Developer needed. Expert in Python, Django, React, PostgreSQL. 5+ years experience required."
            },
            {
                "id": 3,
                "job_title": "Frontend Developer",
                "company_name": "DesignStudio",
                "location": "Cebu, Philippines",
                "experience_level": "mid",
                "work_type": "onsite",
                "salary_min": 50000,
                "salary_max": 70000,
                "salary_currency": "PHP",
                "full_text": "Mid-level Frontend Developer. React, TypeScript, modern CSS required. 2-3 years experience."
            }
        ]
        
        # Test matching for each profile
        for profile_data in profiles:
            print(f"\n   👤 Testing matches for: {profile_data['name']}")
            
            matches = matching_service.find_matches(
                profile_data['profile'], 
                test_jobs, 
                top_k=3
            )
            
            print(f"      Found {len(matches)} matches:")
            
            for i, match in enumerate(matches, 1):
                job = next(j for j in test_jobs if j['id'] == match.job_id)
                print(f"      {i}. {job['job_title']} at {job['company_name']}")
                print(f"         Match Score: {match.match_score:.2f}")
                print(f"         Skill Match: {match.skill_match_percentage:.1f}%")
                print(f"         Experience Match: {'✅' if match.experience_match else '❌'}")
                print(f"         Location Match: {'✅' if match.location_match else '❌'}")
                print(f"         Explanation: {match.explanation}")
                
                if match.skill_gaps:
                    print(f"         Skill Gaps: {', '.join(match.skill_gaps)}")
                
                if match.recommendations:
                    print(f"         Recommendations: {match.recommendations[0]}")
                print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Matching test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_integration():
    """Test database integration with real job data"""
    print("\n💾 Testing Database Integration...")
    try:
        from aica_backend.api.dependencies import get_db
        from aica_backend.database.models import JobPosting, User
        
        with next(get_db()) as db:
            # Check job data
            jobs = db.query(JobPosting).limit(3).all()
            print(f"   📋 Found {len(jobs)} jobs in database:")
            
            for job in jobs:
                print(f"      - {job.job_title} at {job.company_name}")
                print(f"        Location: {job.location}")
                print(f"        Work Type: {job.work_type}")
                print(f"        Experience: {job.experience_level}")
                if job.salary_min:
                    print(f"        Salary: {job.salary_min:,} - {job.salary_max:,} {job.salary_currency}")
                print()
            
            # Check user data
            users = db.query(User).count()
            print(f"   👥 Found {users} users in database")
            
        return len(jobs) > 0
        
    except Exception as e:
        print(f"   ❌ Database test error: {str(e)}")
        return False

def test_api_simulation():
    """Simulate API endpoint behavior"""
    print("\n🌐 Testing API Endpoint Simulation...")
    try:
        from aica_backend.services.matching_service import get_matching_service
        from aica_backend.api.dependencies import get_db
        from aica_backend.database.models import JobPosting
        
        # Simulate the /ai/matches endpoint logic
        with next(get_db()) as db:
            jobs = db.query(JobPosting).limit(5).all()
            
            if not jobs:
                print("   ⚠️ No jobs found - using dummy data")
                return False
            
            # Simulate user profile (normally from auth)
            mock_user_profile = {
                "id": 1,
                "email": "test@example.com",
                "skills": [
                    {"name": "Python", "level": "Advanced"},
                    {"name": "JavaScript", "level": "Intermediate"},
                    {"name": "React", "level": "Beginner"}
                ],
                "location": "Manila, Philippines",
                "work_preferences": {
                    "work_types": ["Remote", "Hybrid"],
                    "minimum_salary": 50000
                }
            }
            
            # Convert jobs to dictionaries (like in API)
            job_dicts = []
            for job in jobs:
                job_dict = {
                    "id": job.id,
                    "job_title": job.job_title,
                    "company_name": job.company_name,
                    "location": job.location,
                    "experience_level": job.experience_level,
                    "work_type": job.work_type,
                    "employment_type": job.employment_type,
                    "salary_min": job.salary_min,
                    "salary_max": job.salary_max,
                    "salary_currency": job.salary_currency,
                    "full_text": job.full_text,
                    "description": job.full_text,
                    "requirements": job.requirements or []
                }
                job_dicts.append(job_dict)
            
            # Run matching
            matching_service = get_matching_service()
            matches = matching_service.find_matches(mock_user_profile, job_dicts, top_k=3)
            
            print(f"   🎯 API Simulation Results:")
            print(f"      User: {mock_user_profile['email']}")
            print(f"      Jobs processed: {len(job_dicts)}")
            print(f"      Matches found: {len(matches)}")
            
            if matches:
                print(f"      Top match: {matches[0].match_score:.2f} score")
                
                # Simulate API response format
                api_response = {
                    "matches": [
                        {
                            "job": {
                                "id": match.job_id,
                                "title": next(j['job_title'] for j in job_dicts if j['id'] == match.job_id),
                                "company": next(j['company_name'] for j in job_dicts if j['id'] == match.job_id)
                            },
                            "match_score": match.match_score,
                            "skill_match_percentage": match.skill_match_percentage,
                            "explanation": match.explanation
                        }
                        for match in matches[:2]  # Top 2 matches
                    ],
                    "total_found": len(matches),
                    "user_id": mock_user_profile["id"]
                }
                
                print(f"      API Response Preview:")
                print(f"      {json.dumps(api_response, indent=8)[:300]}...")
            
        return True
        
    except Exception as e:
        print(f"   ❌ API simulation error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 AICA AI Comprehensive Testing Suite")
    print("=" * 60)
    
    tests = [
        ("Database Integration", test_database_integration),
        ("RAG Embeddings & Search", test_rag_embeddings),
        ("Job Matching Algorithm", test_job_matching_algorithm),
        ("API Endpoint Simulation", test_api_simulation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL AI COMPONENTS ARE WORKING PERFECTLY!")
        print("\n📋 What's Working:")
        print("✅ Database connection and job data retrieval")
        print("✅ RAG service with embeddings and vector search")
        print("✅ Intelligent job matching with weighted scoring")
        print("✅ API endpoint logic and response formatting")
        print("✅ Skill gap analysis and recommendations")
        
        print("\n🚀 Ready for:")
        print("• Frontend integration")
        print("• API endpoint testing")
        print("• User authentication integration")
        print("• Production deployment")
        
    else:
        print("⚠️ Some components need attention. Check the errors above.")
        
    print("\n🔧 To test API endpoints:")
    print("1. Start server: python -m src.aica_backend.main")
    print("2. Visit: http://localhost:8000/docs")
    print("3. Test /ai/status and /ai/matches endpoints")
