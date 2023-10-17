from enum import Enum
from pydantic import BaseModel
from app.models.shop import *

class NewShop(BaseModel):
    name: str
    number: str
    floorid: int
    clientid: int
    area: str


class UpdateShop(BaseModel):
    name: str
    number: str
    floorid: int
    clientid: int
    area: str

        
