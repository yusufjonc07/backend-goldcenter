from pydantic import BaseModel, Field
from app.models.parkingZone import *


class NewParkingZone(BaseModel):
    name: str
    hourlyFee: float = Field(..., gt=0)


class UpdateParkingZone(BaseModel):
    name: str
    hourlyFee: float = Field(..., gt=0)