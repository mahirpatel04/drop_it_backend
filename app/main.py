from fastapi import FastAPI
from app.database import engine, Base
from .routers import auth_router, base_router
from .core import settings, logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(auth_router)
app.include_router(base_router)

Base.metadata.create_all(bind=engine)