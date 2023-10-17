from enum import Enum
from pydantic import BaseModel

class NewNotification(BaseModel):
    title: str
    body: str
    imgurl: str
    user_id: int


class UpdateNotification(BaseModel):
    title: str
    body: str
    imgurl: str
    user_id: int

        
class MessageSchema(BaseModel):
    title: str
    body: str
    imgurl: str