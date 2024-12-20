from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base
import pydantic

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    birthdate = Column(DateTime, nullable=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    drops = Column(ARRAY(Integer), nullable=True)
    private = Column(Boolean, default = False)
    