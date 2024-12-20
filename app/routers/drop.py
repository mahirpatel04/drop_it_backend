from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from app.database import engine, Base, get_db
from app.models import Drop, User
from app.schemas import CreateDropRequest
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
from .auth import get_current_user
from fastapi.logger import logger
from geopy.distance import geodesic

from ..services import *

router = APIRouter(
    prefix='',
    tags=['base']
)

@router.get("/")
def get_user(
    user: User = Depends(get_current_user),
):
    logger.info(f"User {user.id} fetching themselves")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return {"message": user.username}

@router.post("/create_drop")
async def create_drop_endpoint(
    create_drop_request: CreateDropRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    drop = create_drop(create_drop_request, user, db)
    return {"id": drop.id, "content": drop.content, "latitude": drop.latitude, "longitude": drop.longitude}

@router.delete("/remove_drop")
async def remove_drop_endpoint(
    drop_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    drop = remove_drop(drop_id, user, db)
    if not drop:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Drop not found")
    return {"message": "successful"}

@router.get("/get_drops")
async def get_drops_endpoint(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    drops = get_drops(user, db)
    return [{"id": drop.id, "content": drop.content} for drop in drops]

@router.get("/get_drops_nearby")
async def get_drops_nearby_endpoint(
    latitude: float,
    longitude: float,
    radius_km: float = 10.0,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    nearby_drops = get_drops_nearby(latitude, longitude, radius_km, db)
    return [
        {"id": drop.id, "content": drop.content, "latitude": drop.latitude, "longitude": drop.longitude}
        for drop in nearby_drops
    ]
