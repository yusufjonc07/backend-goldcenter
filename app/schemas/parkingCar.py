from datetime import datetime
from pydantic import BaseModel, validator
from app.models.parkingCar import *

class NewParkingCar(BaseModel):
    number: str
    parkingZoneId: int
    enteredAt: datetime

class UpdateParkingCar(BaseModel):
    number: str
    exitedAt: datetime

  
        
