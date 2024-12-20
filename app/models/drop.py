from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base
from datetime import datetime, timezone

class Drop(Base):
    __tablename__ = "drops"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String(500))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)