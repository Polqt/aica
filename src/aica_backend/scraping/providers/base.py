from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseProvider(ABC):
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.base_url = config.get('base_url', '')
        self.rate_limit = config.get('rate_limit', 10)
        self.active = config.get('active', True)
    
    def test_scraping(self, url: Optional[str] = None) -> Dict[str, Any]:
        try:
            test_url = url or self.get_test_url()
            if not test_url:
                return {
                    "success": False,
                    "errors": ["No test URL available"]
                }

            result = self.scrape_job_details(test_url)
            
            return {
                "success": result is not None,
                "data": result or {},
                "errors": [] if result else ["Failed to scrape test URL"]
            }
            
        except Exception as e:
            logger.error(f"Test scraping failed for {self.name}: {str(e)}")
            return {
                "success": False,
                "data": {},
                "errors": [str(e)]
            }
    
    def _create_test_result(self, success: bool, data: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
        return {
            "success": success,
            "data": data,
            "errors": errors
        }
    
    def is_active(self) -> bool:
        return self.active
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "base_url": self.base_url,
            "rate_limit": self.rate_limit,
            "active": self.active,
        }
