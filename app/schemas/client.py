from enum import Enum
from pydantic import BaseModel
from app.models.client import *

class NewClient(BaseModel):
    firstname: str
    lastname: str
    phonenumber: int
    passportserianumber: str
    inn: str


class UpdateClient(BaseModel):
    firstname: str
    lastname: str
    phonenumber: int
    passportserianumber: str
    inn: str

        
