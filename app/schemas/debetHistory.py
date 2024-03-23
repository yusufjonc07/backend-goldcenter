from enum import Enum
from pydantic import BaseModel
from app.models.debetHistory import *


class NewDebethistory(BaseModel):
    comment: str
    regularexpenceid: int
    value: float


class UpdateDebethistory(BaseModel):
    comment: str
    regularexpenceid: int
    value: float
