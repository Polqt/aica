import os
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

class JobDataStorage:
    def __init__(self, storage_dir: str = "data/scraped_jobs"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    
    def save_jobs_urls(self, job_urls: List[str], site_name: str) -> str:
        """
        Save job URLs to JSON file - specifically for URL lists
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{site_name}__jobs__{timestamp}.json"
        filepath = self.storage_dir / filename
        
        data = {
            "metadata": {
                "site": site_name,
                "scraped_at": datetime.now().isoformat(),
                "total_urls": len(job_urls),
                "data_type": "job_urls"
            },
            "job_urls": job_urls
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
        
    def save_jobs_detailed(self, jobs_data: List[Dict[str, Any]], site_name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Group into dated subfolder: storage/scraped_jobs/{site}/{YYYYMMDD}/...
        dated_dir = self.storage_dir / site_name / datetime.now().strftime("%Y%m%d")
        dated_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{site_name}_structured__jobs__{timestamp}.json"
        filepath = dated_dir / filename
        
        total_jobs = len(jobs_data)
        successful_extractions = sum(1 for job in jobs_data if job.get('extraction_quality_score', 0) > 0.5)
        avg_quality_score = sum(job.get('extraction_quality_score', 0) for job in jobs_data) / total_jobs if total_jobs > 0 else 0
        
        # Structured JSON ouput
        data = {
            "metadata": {
                "site": site_name,
                "scraped_at": datetime.now().isoformat(),
                "total_jobs": len(jobs_data),
                "successful_extractions": successful_extractions,
                "average_quality_score": avg_quality_score,
                "data_type": "detailed_jobs",
                "extraction_summary": {
                    "jobs_with_title": sum(1 for job in jobs_data if job.get("job_title")),
                    "jobs_with_company": sum(1 for job in jobs_data if job.get("company_name")),
                    "jobs_with_location": sum(1 for job in jobs_data if job.get("location")),
                    "jobs_with_salary": sum(1 for job in jobs_data if job.get("salary_min") or job.get("salary_max")),
                    "jobs_with_skills": sum(1 for job in jobs_data if job.get('technical_skills'))
                }
            },
            "jobs": jobs_data
        }
        
        tmp = filepath.with_suffix(".tmp")
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, filepath)
        
        return str(filepath)

    def load_jobs_from_file(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def validate_json_file(self, filepath: str) -> Dict[str, Any]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            validation_result = {
                "valid": True,
                "file_size_mb": os.path.getsize(filepath) / (1024 * 1024),
                "has_metadata": "metadata" in data,
                "data_type": data.get("metadata", {}).get("data_type", "unknown"),
                "total_items": 0,
                "errors": []
            }
            
            if "metadata" in data:
                metadata = data["metadata"]
                if "job_urls" in data:
                    validation_result["total_items"] = len(data["job_urls"])
                elif "jobs" in data:
                    validation_result["total_items"] = len(data["jobs"])
            else:
                validation_result["errors"].append("Missing metadata section")
                validation_result["valid"] = False

            return validation_result
        except json.JSONDecoder as e:
            return {
                "valid": False,
                "error": f"Invalid JSON: {str(e)}",
                "file_size_mb": os.path.getsize(filepath) / (1024 * 1024) if os.path.exists(filepath) else 0
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"File error: {str(e)}",
                "file_size_mb": 0
            }