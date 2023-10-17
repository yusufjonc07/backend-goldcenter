from enum import Enum
from pydantic import BaseModel
from app.models.attandance import *

class NewAttandance(BaseModel):
    type: str
    employeeid: int
    worktime: str
    authorizator: int
    created_at: str


class UpdateAttandance(BaseModel):
    type: str
    employeeid: int
    worktime: str
    authorizator: int
    created_at: str

        
