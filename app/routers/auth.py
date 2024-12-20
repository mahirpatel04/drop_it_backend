from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

from app.core import settings, logger
from app.schemas import UserResponse, CreateUserRequest, Token
from app.services import *
from app.utils import AuthenticationError

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/create-user', response_model=UserResponse)
async def create_user_endpoint(
    create_user_request: CreateUserRequest, 
    db: Session = Depends(get_db)
):
    try:
        user = create_user(create_user_request, bcrypt_context, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during user creation: {repr(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        token = create_access_token(user.email, user.id, timedelta(hours=12))
        return Token(access_token=token, token_type='bearer')
    
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during login: {repr(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")