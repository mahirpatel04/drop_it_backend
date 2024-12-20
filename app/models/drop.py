from sqlalchemy import Column, Integer, String, ForeignKey, Float

from app.database import Base

class Drop(Base):
    __tablename__ = "drops"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String(500))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)