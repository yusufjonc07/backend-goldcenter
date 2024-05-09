from pydantic import BaseModel
from app.models.contragent import *


class NewContragent(BaseModel):
    name: str
    categoryId: int


class UpdateContragent(BaseModel):
    name: str
    categoryId: int
