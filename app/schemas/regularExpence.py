from pydantic import BaseModel
from app.models.regularExpence import *
from app.schemas.enums import ExpenceTypes

class NewRegularexpence(BaseModel):
    name: str
    branchid: int

class UpdateRegularexpence(BaseModel):
    name: str
    branchid: int

        
