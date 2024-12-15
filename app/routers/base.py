from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from app.database.database import engine, Base, get_db
from app.models import Drop, User
from app.schemas import CreateDropRequest
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
from .auth import get_current_user
from fastapi.logger import logger

router = APIRouter(
    prefix='',
    tags=['base']
)

@router.get("/hello")
def hello():
    return {"content": "hello"}

@router.get("/")
def get_user(
    user: User = Depends(get_current_user),
):
    logger.info(f"User {user.id} fetching themselves")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return {"message": user.username}


@router.post("/create_drop")
async def create_drop(
    create_drop_request: CreateDropRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create the drop
    drop = Drop(content=create_drop_request.content, user_id=user.id)
    logger.info(f"Received content: {create_drop_request.content}")
    if user.drops is None:
        user.drops = []
    
    db.add(drop)
    db.commit()
    
    user.drops = func.array_append(user.drops, drop.id)
    
    # Commiting the db
    db.commit()
    
    return {drop.id: drop.content}

@router.delete("/remove_drop")
async def remove_drop(
    drop_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
  drop_obj = db.query(Drop).filter(Drop.id == drop_id).filter(Drop.user_id == user.id).first()
  if drop_obj:
      db.delete(drop_obj)
      db.commit()
      return {"message": "succesful"}
  else:
      return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Drop not found")

@router.get("/get_drops")
async def get_drops(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user.drops:
        return {"message": "No drops made"}
    
    # Fetch all drops for the user in one query
    drops = db.query(Drop).filter(Drop.user_id == user.id, Drop.id.in_(user.drops)).all()
    
    # Format the response
    result = [{"id": drop.id, "content": drop.content} for drop in drops]
    return result
