from pydantic import BaseModel
from typing import List, Optional
import datetime


class CreateUserRequest(BaseModel):
    first_name: str
    username: str
    email: str
    password: str
    birthdate: str
    private: bool

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    id: int
    first_name: Optional[str]
    username: str
    email: str
    drops: Optional[List[int]]
    private: bool

    class Config:
        from_attributes = True
