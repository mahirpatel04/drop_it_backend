from pydantic import BaseModel


class CreateDropRequest(BaseModel):
    content: str
    
class SampleResponse(BaseModel):
    content: str