from enum import Enum
from pydantic import BaseModel
from app.models.salary import *
from typing import List


class UpdateSalary(BaseModel):
    calcwage: float


class SalaryIdList(BaseModel):
    ids: List[int]