from pydantic import BaseModel
from app.models.task import *
from app.schemas.enums import TaskTypes

class NewTask(BaseModel):
    context: str
    type: TaskTypes
    forrole: ChatTypes
    replyid: int

class UpdateTask(BaseModel):
    type: str
    userid: int
    forrole: str
    branchid: int
    replyid: int
    createdat: str
    updated_at: str

        
