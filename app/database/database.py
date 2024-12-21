from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core import settings  # Import settings from your config module

# Use the DATABASE_URL from the config settings
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()