from enum import Enum
from typing import Optional
from pydantic import BaseModel
from app.models.user import *

class NewUser(BaseModel):
    userrole: str
    username: str
    password: str
    disabled: bool
    branchid: int
    employeeid: int


class UpdateUser(BaseModel):
    userrole: str
    username: str
    password: Optional[str] = ""
    disabled: bool
    branchid: int
    employeeid: int

        
