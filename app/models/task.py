from sqlalchemy import Column, Enum, Integer, func, String, ForeignKey
from app.schemas.enums import ChatTypes, MessageTypes
from databases.main import Base
from sqlalchemy.orm import relationship
from app.models.user import *
from app.models.branch import *

class Task(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    context = Column(String, default=False)
    fileName = Column(Text, default=False)
    userId = Column(Integer, default=False)
    forRole = Column(Enum(ChatTypes), default=False)
    branchId = Column(Integer, ForeignKey('branch.id'), default=False)
    createdAt = Column(DateTime, nullable=False, default=func.now())

    completedAt = Column(DateTime, nullable=True)
    responseText =  Column(String, nullable=True)
    responseType = Column(Enum(MessageTypes), nullable=True)
    responseFileName = Column(Text, nullable=False)
    responseUserId = Column(Integer, nullable=False)

    
    user = relationship('User', foreign_keys=[userId], backref='given_tasks')
    responseUser = relationship('User', foreign_keys=[responseUserId], backref='given_tasks')
    branch = relationship('Branch', backref='messages')

   
    
