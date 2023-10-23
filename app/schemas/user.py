from enum import Enum
from typing import Optional
from pydantic import BaseModel
from app.models.user import *

class NewUser(BaseModel):
    username: str
    password: str
    employeeid: int


class UpdateUser(BaseModel):
    userrole: str
    username: str
    password: Optional[str] = ""
    disabled: bool

        
