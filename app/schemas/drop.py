from pydantic import BaseModel

class CreateDropRequest(BaseModel):
    content: str