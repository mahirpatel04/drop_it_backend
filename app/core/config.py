from pydantic import BaseSettings
import os

DATABASE_URL = os.getenv("DATABASE_URL")

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = DATABASE_URL

    class Config:
        env_file = ".env"

settings = Settings()