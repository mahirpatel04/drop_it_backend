from fastapi import FastAPI, Depends, HTTPException, status
from app.database import engine, Base, get_db
from app.models import Drop, User
from app.schemas import CreateDropRequest
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .routers import auth_router, base_router
from fastapi.logger import logger

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(auth_router)
app.include_router(base_router)

Base.metadata.create_all(bind=engine)