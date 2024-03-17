from enum import Enum
from pydantic import BaseModel, Field
from app.models.income import *
from app.schemas.enums import IncomeType
from typing import Optional


class NewIncome(BaseModel):
    regularIncomeId: Optional[int] = 0
    clientId: Optional[int] = 0
    value: float = Field(..., gt=0, lt=1000000000)
    moneyFormId: int
    comment: str
    type: Optional[IncomeType] = 'rent'
    forYear: int
    forMonth: int


class UpdateIncome(BaseModel):
    clientId: int
    value: float = Field(..., gt=0, lt=1000000000)
    moneyFormId: int
    comment: str
    type: Optional[IncomeType] = 'rent'
    forYear: int
    forMonth: int
