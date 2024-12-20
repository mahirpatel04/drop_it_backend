from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db, SessionLocal
from app.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.logger import logger

from ..schemas import UserResponse, CreateUserRequest, Token


def create_user(create_user_request: CreateUserRequest, db: Session):
    user = User(
        first_name = create_user_request.first_name,
        birthdate = create_user_request.birthdate,
        username = create_user_request.username,
        email = create_user_request.email,
        password = create_user_request.password,
        private = create_user_request.private
    )