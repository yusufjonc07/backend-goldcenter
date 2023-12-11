from enum import Enum
from pydantic import BaseModel
from app.models.salary import *


class UpdateSalary(BaseModel):
    calcwage: float