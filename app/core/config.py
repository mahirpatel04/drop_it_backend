from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    VERSION: str = "0.1.0"
    DATABASE_URL: str  # Marked as required; ensure `.env` provides it or handle validation

    class Config:
        env_file = ".env"  # Automatically loads environment variables from `.env`

# Instantiate settings
settings = Settings()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="[SERVER LOGGER] %(levelname)s @ %(asctime)s: %(message)s",  # Define log message format
)

logger = logging.getLogger(__name__)  # Create a named logger if needed for modular logging