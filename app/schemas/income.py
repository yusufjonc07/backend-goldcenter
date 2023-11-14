from enum import Enum
from pydantic import BaseModel
from app.models.income import *

class NewIncome(BaseModel):
    clientId: int
    value: float
    moneyFormId: int
    comment: str


class UpdateIncome(BaseModel):
    clientId: int
    value: float
    moneyFormId: int
    comment: str

        
