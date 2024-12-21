from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import logging

class Settings(BaseSettings):
    PROJECT_NAME: str = "DropIt"
    VERSION: str = "0.1.0"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    TEST_DATABASE_URL: str
    
    # Use the ConfigDict to replace the class-based Config
    model_config = ConfigDict(env_file = ".env")

# Instantiate settings
settings = Settings()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="[SERVER LOGGER] %(levelname)s @ %(asctime)s: %(message)s",  # Define log message format
)

logger = logging.getLogger(__name__)  # Create a named logger if needed for modular logging