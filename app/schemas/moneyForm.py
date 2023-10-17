from enum import Enum
from pydantic import BaseModel
from app.models.moneyForm import *

class NewMoneyform(BaseModel):
    name: str


class UpdateMoneyform(BaseModel):
    name: str

        
