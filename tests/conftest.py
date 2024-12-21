import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database, database_exists
from alembic.config import Config
from alembic import command

from app.main import app
from app.database import Base, get_db
from app.core import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

# Create a testing engine and session factory
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    drop_database(TEST_DATABASE_URL)


@pytest.fixture(scope="function")
def db_session():
    # Create a new session for each test
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# Override FastAPI's dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
