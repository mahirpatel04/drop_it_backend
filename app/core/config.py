from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"

    class Config:
        env_file = ".env"

settings = Settings()