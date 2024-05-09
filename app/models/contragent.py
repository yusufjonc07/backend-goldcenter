from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.floor import *
from app.models.branch import *


class Contragent(Base):
    __tablename__ = "contragent"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    balance = Column(Numeric, default=0)
    categoryId = Column(Integer, ForeignKey('category.id'))

    category = relationship('Category', backref='contragents')
