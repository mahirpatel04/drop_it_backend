from fastapi import FastAPI, Depends, HTTPException
from database import engine, Base, get_db
from models import Drop, User
from schema import CreateDropRequest, SampleResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from auth import router as auth_router, get_current_user
from fastapi.logger import logger

app = FastAPI()
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def get_user(
    user: User = Depends(get_current_user),
):
    logger.info(f"User {user.id} fetching themselves")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return user


@app.post("/create_drop")
async def create_drop(
    content:str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    drop = Drop(content=content, user_id=user.id)
    db.add(drop)
    db.commit()
    return {drop.id: drop.content}

