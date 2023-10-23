from email.policy import default
from sqlalchemy import Column, Enum, Integer, text, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from app.schemas.enums import ChatTypes, MessageTypes
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.user import *
from app.models.branch import *


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    context = Column(String)
    type = Column(Enum(MessageTypes))
    userId = Column(Integer, ForeignKey('user.id'), default=0)
    forRole = Column(Enum(ChatTypes))
    branchId = Column(Integer, ForeignKey('branch.id'), default=0)
    replyId = Column(Integer, default=0, nullable=True)
    createdAt = Column(TIMESTAMP, nullable=False, default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True, default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))

    user = relationship('User', backref='messages')
    branch = relationship('Branch', backref='messages')
