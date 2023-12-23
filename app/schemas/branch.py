from enum import Enum
from pydantic import BaseModel
from app.models.branch import *


class NewBranch(BaseModel):
    name: str
    address: str
    dollar: float
    electrPrice: float


class UpdateBranch(BaseModel):
    name: str
    address: str
    dollar: float
    electrPrice: float
