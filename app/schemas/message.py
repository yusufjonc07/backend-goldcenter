from enum import Enum
from pydantic import BaseModel
from app.models.message import *

class NewMessage(BaseModel):
    type: str
    userid: int
    forrole: str
    branchid: int
    replyid: int
    createdat: str
    updated_at: str


class UpdateMessage(BaseModel):
    type: str
    userid: int
    forrole: str
    branchid: int
    replyid: int
    createdat: str
    updated_at: str

        
