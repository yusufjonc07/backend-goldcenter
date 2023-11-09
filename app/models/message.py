from email.policy import default
from sqlalchemy import Column, Enum, Integer, text, and_, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from app.schemas.enums import ChatTypes, MessageTypes
from databases.main import Base
from sqlalchemy.orm import relationship, aliased
from app.models.user import *
from app.models.branch import *

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    context = Column(String, nullable=True)
    fileName = Column(Text, nullable=True)
    isViewed = Column(Boolean, default=False)
    userId = Column(Integer, ForeignKey('user.id'), default=0)
    forRole = Column(Enum(ChatTypes))
    branchId = Column(Integer, ForeignKey('branch.id'), default=0)
    replyId = Column(Integer, nullable=True)
    type = Column(Enum(MessageTypes), nullable=False)
    createdAt = Column(TIMESTAMP, nullable=False, default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True, default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    
    user = relationship('User', backref='messages')
    branch = relationship('Branch', backref='messages')

   
    
