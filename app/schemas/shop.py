from enum import Enum
from typing import Optional
from pydantic import BaseModel
from app.models.shop import *

class NewShop(BaseModel):
    name: str
    number: str
    floorId: int
    area: float


class UpdateShop(BaseModel):
    name: str
    number: str
    floorId: int
    area: float

        
