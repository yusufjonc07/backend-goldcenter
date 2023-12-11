from enum import Enum
from pydantic import BaseModel
from app.models.attandance import *

class NewAttandance(BaseModel):
    type: str
    employeeId: int
    authorizator: str
    created_at: str


class UpdateAttandance(BaseModel):
    type: str
    employeeid: int
    authorizator: str
    created_at: str

        
