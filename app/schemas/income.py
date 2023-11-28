from enum import Enum
from pydantic import BaseModel, Field
from app.models.income import *

class NewIncome(BaseModel):
    clientId: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyFormId: int
    comment: str


class UpdateIncome(BaseModel):
    clientId: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyFormId: int
    comment: str

        
