from sqlalchemy.orm import Session
from sqlalchemy import func
from geopy.distance import geodesic
from app.models import Drop, User
from app.schemas import CreateDropRequest

def create_drop(create_drop_request: CreateDropRequest, user: User, db: Session):
    drop = Drop(
        content=create_drop_request.content,
        user_id=user.id,
        latitude=create_drop_request.latitude,
        longitude=create_drop_request.longitude,
    )
    db.add(drop)
    db.commit()
    user.drops = func.array_append(user.drops, drop.id)
    db.commit()
    return drop

def remove_drop(drop_id: int, user: User, db: Session):
    drop = db.query(Drop).filter(Drop.id == drop_id, Drop.user_id == user.id).first()
    if not drop:
        return None
    db.delete(drop)
    db.commit()
    return drop

def get_drops(user: User, db: Session):
    if not user.drops:
        return []
    return db.query(Drop).filter(Drop.user_id == user.id, Drop.id.in_(user.drops)).all()

def get_drops_nearby(latitude: float, longitude: float, radius_km: float, db: Session):
    all_drops = db.query(Drop).all()  # Get all drops
    nearby_drops = []

    for drop in all_drops:
        drop_location = (drop.latitude, drop.longitude)
        user_location = (latitude, longitude)
        distance = geodesic(user_location, drop_location).km

        if distance <= radius_km:
            # Append the Drop object itself
            drop.distance = distance  # You can add the distance as an attribute if you need it in the ORM object
            nearby_drops.append(drop)

    return sorted(nearby_drops, key=lambda x: geodesic((latitude, longitude), (x.latitude, x.longitude)).km)