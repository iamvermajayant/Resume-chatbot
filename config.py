from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    ALLOWED_ORIGINS: list[str] = ["*"]
    CHROMA_DB_DIR: str = "./chroma_db"

settings = Settings()