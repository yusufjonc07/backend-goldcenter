from enum import Enum
from pydantic import BaseModel, Field
from app.models.income import *
from app.schemas.enums import IncomeType
from typing import Optional


class NewIncome(BaseModel):
    clientId: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyFormId: int
    comment: str
    type: Optional[IncomeType] = 'rent'
    forYear: int
    forMonth: int
    electrLastAmount: Optional[float] = 0
    electrAmount: Optional[float] = 0


class UpdateIncome(BaseModel):
    clientId: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyFormId: int
    comment: str
    type: Optional[IncomeType] = 'rent'
    forYear: int
    forMonth: int
    electrLastAmount: Optional[float] = 0
    electrAmount: Optional[float] = 0
