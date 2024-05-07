from sqlalchemy import Column, Date, Integer, Numeric,  Boolean, ForeignKey, func
from databases.main import Base
from sqlalchemy.orm import relationship
from app.models.floor import *
from sqlalchemy.dialects.mysql import DOUBLE


class ClientFee(Base):
    __tablename__ = "clientFee"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    clientId = Column(Integer, ForeignKey('client.id'))
    value = Column(Numeric, default=0)
    isConfirmed = Column(Boolean, default=False)
    createdAt = Column(Date, default=func.now())
    adPrice = Column(Numeric, default=0)
    electrPrice = Column(Numeric, default=0)
    electrAmount = Column(Numeric, default=0)

    client = relationship('Client')
