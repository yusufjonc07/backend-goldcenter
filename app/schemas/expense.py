from enum import Enum
from pydantic import BaseModel, Field
from app.models.expense import *
from typing import Optional
from datetime import date


class NewExpense(BaseModel):
    type: ExpenceTypes
    employeeId: Optional[int]
    contragentId: Optional[int]
    value: float = Field(..., gt=0)
    moneyFormId: int
    isAvanse: bool
    comment: str = Field(..., min_length=5)


class UpdateExpense(BaseModel):
    type: str
    employeeid: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyformid: int
    comment: str
    isAvanse: bool
    userid: int
    filename: dict
    createdat: str
    branchid: int
    floorid: int


class NewExpenseExcel(BaseModel):
    pnfl: str
    value: float = Field(..., gt=0)
    moneyFormName: str
    isAvanse: bool
    date: date
