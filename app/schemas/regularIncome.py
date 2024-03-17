from enum import Enum
from pydantic import BaseModel
from app.models.regularIncome import *

class NewRegularincome(BaseModel):
    name: str


class UpdateRegularincome(BaseModel):
    name: str

        
