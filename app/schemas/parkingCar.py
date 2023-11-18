from datetime import datetime
from pydantic import BaseModel, validator
from app.models.parkingCar import *

class NewParkingCar(BaseModel):
    number: str
    parkingZoneId: int
    enteredAt: datetime = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

class UpdateParkingCar(BaseModel):
    number: str
    exitedAt: datetime = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')