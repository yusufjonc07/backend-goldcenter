from enum import Enum
from pydantic import BaseModel
from app.models.clientAgreement import *

class NewClientagreement(BaseModel):
    filename: dict
    shopid: int
    clientid: int
    monthlyfee: str
    balance: str
    status: bool


class UpdateClientagreement(BaseModel):
    filename: dict
    shopid: int
    clientid: int
    monthlyfee: str
    balance: str
    status: bool

        
