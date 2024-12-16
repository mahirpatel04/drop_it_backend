from pydantic import BaseModel
from typing import List, Optional

class UserResponse(BaseModel):
    id: int
    first_name: Optional[str]
    username: str
    email: str
    drops: Optional[List[int]]
    private: bool

    class Config:
        from_attributes = True
