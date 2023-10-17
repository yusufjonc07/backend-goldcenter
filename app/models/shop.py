from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.floor import * 
from app.models.client import * 


class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    number = Column(String, default='')
    floorId = Column(Integer, ForeignKey('floor.id'), default=0)
    clientId = Column(Integer, ForeignKey('client.id'), nullable=True)
    area = Column(String, default='')

    floor = relationship('Floor', backref='shops')
    client = relationship('Client', backref='shops')

