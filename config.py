from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (for local development)
try:
    load_dotenv()
    logger.info("Environment variables loaded from .env file")
except Exception as e:
    logger.warning(f"Could not load .env file: {str(e)}")

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    ALLOWED_ORIGINS: list[str] = ["*"]
    CHROMA_DB_DIR: str = "./chroma_db"
    
    class Config:
        env_file = ".env"

try:
    settings = Settings()
    logger.info("Settings initialized successfully")
    logger.info(f"CHROMA_DB_DIR: {settings.CHROMA_DB_DIR}")
    logger.info(f"ALLOWED_ORIGINS: {settings.ALLOWED_ORIGINS}")
    
    # Verify critical environment variables
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is required but not set")
    logger.info("GEMINI_API_KEY is set")
    
except Exception as e:
    logger.error(f"Failed to initialize settings: {str(e)}")
    logger.error("Available environment variables:")
    for key, value in os.environ.items():
        if 'GEMINI' in key or 'ALLOWED' in key or 'CHROMA' in key:
            logger.error(f"  {key}: {value}")
    raise