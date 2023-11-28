from enum import Enum
from pydantic import BaseModel, Field
from app.models.expense import *

class NewExpense(BaseModel):
    type: str
    employeeid: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyformid: int
    comment: str
    userid: int
    filename: dict
    createdat: str
    branchid: int
    floorid: int


class UpdateExpense(BaseModel):
    type: str
    employeeid: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyformid: int
    comment: str
    userid: int
    filename: dict
    createdat: str
    branchid: int
    floorid: int

        
