from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class BaseProvider(ABC):
    """Base class for all scraping providers."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.rate_limit = config.get('rate_limit', 10)
        self.active = config.get('active', True)

    def is_active(self) -> bool:
        """Check if provider is active."""
        return self.active

    @abstractmethod
    async def scrape_jobs(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape job listings from given URLs."""
        pass

    @abstractmethod
    async def get_supported_sites(self) -> List[str]:
        """Get list of supported site domains."""
        pass

    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to provider services."""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get provider information."""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "active": self.active,
            "config": {k: v for k, v in self.config.items()
                      if not k.startswith('_') and k != 'api_key'}
        }
    