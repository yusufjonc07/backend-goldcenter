from enum import Enum
from pydantic import BaseModel
from app.models.parkingZone import *


class NewParkingZone(BaseModel):
    name: str
    hourlyfee: float


class UpdateParkingZone(BaseModel):
    name: str
    hourlyfee: float
