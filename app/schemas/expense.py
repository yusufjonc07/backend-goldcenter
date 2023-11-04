from enum import Enum
from pydantic import BaseModel
from app.models.expense import *

class NewExpense(BaseModel):
    type: str
    employeeid: int
    value: float
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
    value: float
    moneyformid: int
    comment: str
    userid: int
    filename: dict
    createdat: str
    branchid: int
    floorid: int

        
