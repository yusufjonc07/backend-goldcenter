from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.shop import * 
from app.models.client import * 


class Clientagreement(Base):
    __tablename__ = "clientAgreement"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fileName = Column(Text, default='')
    shopId = Column(Integer, ForeignKey('shop.id'), default=0)
    clientId = Column(Integer, ForeignKey('client.id'), default=0)
    monthlyFee = Column(String, default='')
    balance = Column(String, default='')
    status = Column(Boolean, default=False)

    shop = relationship('Shop', backref='clientAgreements')
    client = relationship('Client', backref='clientAgreements')

