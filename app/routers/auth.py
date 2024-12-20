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

from ..schemas import UserResponse, CreateUserRequest, Token, GeneralResponse
from ..services import create_user

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'DROPAPP_BACKEND_PRODUCTION_f23o_ci;ru2qipwufdh_ilqwefhqwie_dh'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post('/create-user')
async def create_user_endpoint(
    create_user_request: CreateUserRequest, 
    db: Session = Depends(get_db)
):
    try:
        user = create_user(create_user_request, db)
        return GeneralResponse(detail=user.username)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.email, user.id, timedelta(hours=12))
    return Token(access_token=token, token_type='bearer')

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    return user if user and bcrypt_context.verify(password, user.password) else False

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'exp': (datetime.now(timezone.utc) + expires_delta)
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], session: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        fetched_user = session.query(User).get(user_id)
        if not fetched_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return fetched_user 
    except JWTError as e:
        logger.info(f"JWT ERROR: {repr(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
@router.get('/user', response_model= UserResponse)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user