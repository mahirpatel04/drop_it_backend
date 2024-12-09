from fastapi import FastAPI, Depends, HTTPException, status
from app.database import engine, Base, get_db
from app.models import Drop, User
from app.schema import CreateDropRequest, SampleResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .auth import router as auth_router, get_current_user
from fastapi.logger import logger

app = FastAPI()
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)

@app.get("/hello")
def hello():
    return {"content": "vedaNTHP1"}



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
    content: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    drop = Drop(content=content, user_id=user.id)
    db.add(drop)
    db.commit()
    return {drop.id: drop.content}

@app.delete("/remove_drop")
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
