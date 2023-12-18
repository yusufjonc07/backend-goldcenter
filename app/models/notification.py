from sqlalchemy import Column, Integer, ForeignKey, String
from app.schemas.enums import NotificationTypes
from databases.main import Base
from sqlalchemy.orm import relationship
from app.models.user import * 


class Notification(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    context = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    type = Column(Enum(NotificationTypes), nullable=False)
    isViewed = Column(Boolean, default=False)
    isSend = Column(Boolean, default=False)

    user = relationship('User', backref='notifications')


    

