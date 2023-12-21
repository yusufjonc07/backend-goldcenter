from pydantic import BaseModel
from app.models.regularExpence import *
from app.schemas.enums import ExpenceTypes

class NewRegularexpence(BaseModel):
    name: str

class UpdateRegularexpence(BaseModel):
    name: str

        
