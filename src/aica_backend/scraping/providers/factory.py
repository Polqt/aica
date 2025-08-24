from typing import Dict, Any
from .base import BaseProvider
from .crawl4ai_provider import Crawl4AIProvider

class ScrapingProviderFactory:
    
    _providers = {
        'crawl4ai': Crawl4AIProvider,
    }
    
    @classmethod
    def create_provider(cls, provider_name: str, config: Dict[str, Any]) -> BaseProvider:
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_name}. Available: {list(cls._providers.keys())}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(config)
    
    @classmethod
    def get_available_providers(cls) -> list:
        return list(cls._providers.keys())