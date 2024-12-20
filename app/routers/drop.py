from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models import User
from app.schemas import CreateDropRequest
from app.services import *

router = APIRouter(
    prefix='',
    tags=['base']
)

@router.post("/create_drop")
async def create_drop_endpoint(
    create_drop_request: CreateDropRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        drop = create_drop(create_drop_request, user, db)
        return {"id": drop.id, "content": drop.content, "latitude": drop.latitude, "longitude": drop.longitude}
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

@router.delete("/remove_drop")
async def remove_drop_endpoint(
    drop_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        drop = remove_drop(drop_id, user, db)
        return {"message": "successful"}
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

@router.get("/get_drops")
async def get_drops_endpoint(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        drops = get_drops(user, db)
        return [{"id": drop.id, "content": drop.content} for drop in drops]
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

@router.get("/get_drops_nearby")
async def get_drops_nearby_endpoint(
    latitude: float,
    longitude: float,
    radius_km: float = 10.0,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        nearby_drops = get_drops_nearby(latitude, longitude, radius_km, db)
        return [
            {"id": drop.id, "content": drop.content, "latitude": drop.latitude, "longitude": drop.longitude}
            for drop in nearby_drops
        ]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
