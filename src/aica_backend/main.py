import logging
from .api.main import app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "aica_backend.api.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=False,  # Disabled reload to prevent import string requirement
        log_level="info"
    )