from pydantic import BaseModel

class CreateDropRequest(BaseModel):
    content: str
    latitude: float
    longitude: float