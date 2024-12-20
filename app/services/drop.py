from sqlalchemy.orm import Session
from sqlalchemy import func
from geopy.distance import geodesic
from sqlalchemy.exc import SQLAlchemyError

from app.models import Drop, User
from app.schemas import CreateDropRequest

def create_drop(create_drop_request: CreateDropRequest, user: User, db: Session):
    try:
        drop = Drop(
            content=create_drop_request.content,
            user_id=user.id,
            latitude=create_drop_request.latitude,
            longitude=create_drop_request.longitude,
        )
        db.add(drop)
        db.commit()
        
        # Update the user's drops list
        user.drops = func.array_append(user.drops, drop.id)
        db.commit()
        return drop
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Failed to create drop: {str(e)}")

def remove_drop(drop_id: int, user: User, db: Session):
    try:
        drop = db.query(Drop).filter(Drop.id == drop_id, Drop.user_id == user.id).first()
        if not drop:
            raise ValueError("Drop not found or you don't have permission to remove it.")
        db.delete(drop)
        db.commit()
        return drop
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Failed to remove drop: {str(e)}")

def get_drops(user: User, db: Session):
    try:
        if not user.drops:
            return []
        return db.query(Drop).filter(Drop.user_id == user.id, Drop.id.in_(user.drops)).all()
    except SQLAlchemyError as e:
        raise ValueError(f"Failed to get drops: {str(e)}")

def get_drops_nearby(latitude: float, longitude: float, radius_km: float, db: Session):
    try:
        all_drops = db.query(Drop).all()  # Get all drops
        nearby_drops = []

        for drop in all_drops:
            drop_location = (drop.latitude, drop.longitude)
            user_location = (latitude, longitude)
            distance = geodesic(user_location, drop_location).km

            if distance <= radius_km:
                drop.distance = distance  # You can add the distance as an attribute if you need it in the ORM object
                nearby_drops.append(drop)

        if not nearby_drops:
            raise ValueError("No drops found within the specified radius.")

        return sorted(nearby_drops, key=lambda x: geodesic((latitude, longitude), (x.latitude, x.longitude)).km)
    except SQLAlchemyError as e:
        raise ValueError(f"Failed to fetch nearby drops: {str(e)}")
