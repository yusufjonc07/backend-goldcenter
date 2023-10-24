from pydantic import BaseModel
from app.models.floor import *
from app.schemas.enums import FloorTypes

class NewFloor(BaseModel):
    name: str
    number: int
    description: str
    coridorCleaningCost: float
    branchid: int
    type: FloorTypes


class UpdateFloor(BaseModel):
    name: str
    number: int
    description: str
    coridorCleaningCost: float
    branchid: int
    type: FloorTypes

        
