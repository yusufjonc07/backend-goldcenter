from pydantic import BaseModel, Field
from app.models.parkingZone import *


class NewParkingZone(BaseModel):
    name: str
    hourlyfee: float = Field(..., gt=0)


class UpdateParkingZone(BaseModel):
    name: str
    hourlyfee: float = Field(..., gt=0)