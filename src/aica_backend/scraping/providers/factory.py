"""
Scraping Providers Factory

This module manages and creates scraping provider instances.
"""

from typing import Dict, Any, Optional
import logging
from .base import BaseProvider

logger = logging.getLogger(__name__)

class ProviderFactory:
    """
    Factory for creating and managing scraping providers
    """
    
    def __init__(self):
        self._providers = {}
        self._config = {}
        self._register_default_providers()
    
    def _register_default_providers(self):
        """Register default scraping providers"""
        try:
            # Register available providers here
            # For now, we'll have a placeholder structure
            self._config = {
                "jobstreet": {
                    "description": "JobStreet Philippines job scraper",
                    "features": ["job_listings", "job_details", "company_info"],
                    "rate_limit": 20,
                    "active": False,  # Disabled for now
                    "base_url": "https://www.jobstreet.com.ph"
                }
            }
            logger.info("Registered default scraping providers")
        except Exception as e:
            logger.error(f"Failed to register default providers: {str(e)}")
    
    def get_provider(self, name: str) -> Optional[BaseProvider]:
        """Get a provider instance by name"""
        if name not in self._providers:
            return self._create_provider(name)
        return self._providers.get(name)
    
    def _create_provider(self, name: str) -> Optional[BaseProvider]:
        """Create a new provider instance"""
        try:
            if name == "jobstreet":
                # Import and create JobStreet provider
                # For now, return None as it's not implemented yet
                return None
            
            logger.warning(f"Unknown provider: {name}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to create provider {name}: {str(e)}")
            return None
    
    def get_available_providers(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available providers"""
        return self._config.copy()
    
    def get_scraping_config(self) -> Dict[str, Any]:
        """Get current scraping configuration"""
        return {
            "providers": self._config,
            "global_settings": {
                "max_concurrent_requests": 5,
                "request_delay": 1.0,
                "timeout": 30,
                "max_retries": 3
            }
        }
    
    def update_scraping_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update scraping configuration"""
        try:
            if "providers" in config:
                self._config.update(config["providers"])
            
            logger.info("Updated scraping configuration")
            return self.get_scraping_config()
            
        except Exception as e:
            logger.error(f"Failed to update config: {str(e)}")
            raise


# Global factory instance
_provider_factory = None

def get_provider_factory() -> ProviderFactory:
    """Get global provider factory instance"""
    global _provider_factory
    if _provider_factory is None:
        _provider_factory = ProviderFactory()
    return _provider_factory

# Convenience functions
def get_provider(name: str) -> Optional[BaseProvider]:
    """Get a provider by name"""
    return get_provider_factory().get_provider(name)

def get_available_providers() -> Dict[str, Dict[str, Any]]:
    """Get available providers"""
    return get_provider_factory().get_available_providers()

def get_scraping_config() -> Dict[str, Any]:
    """Get scraping configuration"""
    return get_provider_factory().get_scraping_config()

def update_scraping_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Update scraping configuration"""
    return get_provider_factory().update_scraping_config(config)
