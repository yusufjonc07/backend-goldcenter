from app.schemas.enums import CategoryTypes
from pydantic import BaseModel
from app.models.category import *


class NewCategory(BaseModel):
    name: str
    type: CategoryTypes


class UpdateCategory(BaseModel):
    name: str
    type: CategoryTypes
