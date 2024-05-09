from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.contragent import *


class DebetHistory(Base):
    __tablename__ = "debetHistory"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comment = Column(String)
    contragentId = Column(Integer, ForeignKey('contragent.id'))
    createdAt = Column(DateTime, default=func.now())
    value = Column(Numeric)

    contragent = relationship('Contragent', backref='debetHistorys')
