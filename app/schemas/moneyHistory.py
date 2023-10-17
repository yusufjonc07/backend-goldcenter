from enum import Enum
from pydantic import BaseModel
from app.models.moneyHistory import *

class NewMoneyhistory(BaseModel):
    ownertable: str
    ownerid: int
    value: str
    moneyformid: int
    branchid: int
    comment: str
    userid: int
    filename: dict
    createdat: str


class UpdateMoneyhistory(BaseModel):
    ownertable: str
    ownerid: int
    value: str
    moneyformid: int
    branchid: int
    comment: str
    userid: int
    filename: dict
    createdat: str

        
