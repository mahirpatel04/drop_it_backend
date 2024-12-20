from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class CreateUserRequest(BaseModel):
    first_name: str
    username: str
    email: str
    password: str
    birthdate: date
    private: bool
    
    class Config:
        arbitrary_types_allowed = True

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
