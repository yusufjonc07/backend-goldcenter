from enum import Enum
from pydantic import BaseModel
from app.models.shift import *

class NewShift(BaseModel):
    name: str
    workbegintime: str
    period: float


class UpdateShift(BaseModel):
    name: str
    workbegintime: str
    period: float

        
