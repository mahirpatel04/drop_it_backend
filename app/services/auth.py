from sqlalchemy.orm import Session
from app.models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core import logger, settings
from app.schemas import CreateUserRequest
from app.database import get_db
from app.utils import AuthenticationError

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_user(create_user_request: CreateUserRequest, bcrypt_context: CryptContext, db: Session):
    # Check for duplicate username or email
    existing_user = db.query(User).filter(
        (User.username == create_user_request.username) | (User.email == create_user_request.email)
    ).first()
    if existing_user:
        logger.info(f"Duplicate user: Username: \"{existing_user.username}\", Email: \"{existing_user.email}\"")
        raise ValueError("Username or email already exists.")

    user = User(
        first_name=create_user_request.first_name,
        birthdate=create_user_request.birthdate,
        username=create_user_request.username,
        email=create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
        private=create_user_request.private
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt_context.verify(password, user.password):
        raise AuthenticationError("Invalid username or password.")
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = {
        'sub': username,
        'id': user_id,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], session: Annotated[Session, Depends(get_db)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if not username or not user_id:
            raise AuthenticationError("Invalid token payload.")
        user = session.query(User).get(user_id)
        if not user:
            raise AuthenticationError("User not found.")
        return user
    except JWTError as e:
        logger.warning(f"JWT Error: {e}")
        raise AuthenticationError("Token is invalid or expired.")
