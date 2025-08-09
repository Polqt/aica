from typing import Dict, Any, Optional
import logging
from .generator import EmbeddingGenerator

logger = logging.getLogger(__name__)

class EmbeddingModelManager:
    def __init__(self):
        self.models: Dict[str, EmbeddingGenerator] = {}
        self.default_model = None
        
    def load_model(self, name: str, model_path: str, set_as_default: bool = False) -> bool:
        try:
            generator = EmbeddingGenerator(model_name=model_path)
            self.models[name] = generator
            
            if set_as_default or self.default_model is None:
                self.default_model = name
                
            logger.info(f"Loaded embedding model '{name}' from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model '{name}': {str(e)}")
            return False
    
    def get_model(self, name: Optional[str] = None) -> Optional[EmbeddingGenerator]:
        if name is None:
            name = self.default_model
            
        return self.models.get(name)
    
    def list_models(self) -> Dict[str, Dict[str, Any]]:
        model_info = {}
        for name, generator in self.models.items():
            model_info[name] = {
                "model_name": generator.model_name,
                "dimension": generator.get_embedding_dimension(),
                "is_default": name == self.default_model
            }
        return model_info
    
    def unload_model(self, name: str) -> bool:
        if name in self.models:
            del self.models[name]
            if self.default_model == name:
                self.default_model = list(self.models.keys())[0] if self.models else None
            logger.info(f"Unloaded model '{name}'")
            return True
        return False

_model_manager = None

def get_model_manager() -> EmbeddingModelManager:
    global _model_manager
    if _model_manager is None:
        _model_manager = EmbeddingModelManager()
        _model_manager.load_model(
            name="default",
            model_path="sentence-transformers/all-MiniLM-L6-v2",
            set_as_default=True
        )
    return _model_manager
