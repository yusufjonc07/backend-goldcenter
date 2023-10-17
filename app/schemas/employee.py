from enum import Enum
from pydantic import BaseModel
from app.models.employee import *

class NewEmployee(BaseModel):
    firstname: str
    lastname: str
    phonenumber: int
    passportserianumber: str
    salaryquantity: str
    role: str
    agreementfile: dict
    duty: str
    fired: bool
    branchid: int
    shiftid: int


class UpdateEmployee(BaseModel):
    firstname: str
    lastname: str
    phonenumber: int
    passportserianumber: str
    salaryquantity: str
    role: str
    agreementfile: dict
    duty: str
    fired: bool
    branchid: int
    shiftid: int

        
