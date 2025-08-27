from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class BaseProvider(ABC):
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.rate_limit = config.get('rate_limit', 10)
        self.active = config.get('active', True)
    
    
    def is_active(self) -> bool:
        return self.active
    