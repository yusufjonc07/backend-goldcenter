from enum import Enum
from pydantic import BaseModel
from app.models.income import *

class NewIncome(BaseModel):
    type: str
    clientagreementid: int
    value: float
    moneyformid: int
    comment: str
    userid: int
    createdat: str


class UpdateIncome(BaseModel):
    type: str
    clientagreementid: int
    value: float
    moneyformid: int
    comment: str
    userid: int
    createdat: str

        
