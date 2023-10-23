from pydantic import BaseModel
from app.models.message import *

class NewMessage(BaseModel):
    context: str
    type: MessageTypes
    forrole: ChatTypes
    replyid: int

class UpdateMessage(BaseModel):
    type: str
    userid: int
    forrole: str
    branchid: int
    replyid: int
    createdat: str
    updated_at: str

        
