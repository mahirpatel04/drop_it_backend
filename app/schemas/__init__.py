from pydantic import BaseModel

from .drop import *
from .user import *

class GeneralResponse(BaseModel):
    detail: str