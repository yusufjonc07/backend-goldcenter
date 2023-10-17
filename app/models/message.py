from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.user import * 
from app.models.branch import * 


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, default='')
    userId = Column(Integer, ForeignKey('user.id'), default=0)
    forRole = Column(String, default='')
    branchId = Column(Integer, ForeignKey('branch.id'), default=0)
    replyId = Column(Integer, default=0)
    createdAt = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    user = relationship('User', backref='messages')
    branch = relationship('Branch', backref='messages')

