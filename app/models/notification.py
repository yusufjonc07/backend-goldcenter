from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, JSON, Boolean, Text, ForeignKey, func
from databases.main import Base
from sqlalchemy.orm import relationship
from app.models.user import * 


class Notification(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, default='')
    body = Column(JSON)
    imgUrl = Column(String, default='')
    user_id = Column(Integer, ForeignKey('user.id'), default=0)

    user = relationship('User', backref='notifications')

