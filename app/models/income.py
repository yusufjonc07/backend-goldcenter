from sqlalchemy import Column, Integer, Numeric, text, String, ForeignKey, TIMESTAMP
from app.schemas.enums import IncomeType
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.client import *
from app.models.moneyForm import *
from app.models.user import *
from sqlalchemy.dialects.mysql import DOUBLE


class Income(Base):
    __tablename__ = "income"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    clientId = Column(Integer, ForeignKey('client.id'))
    value = Column(Numeric)
    forYear = Column(Integer)
    forMonth = Column(Integer)
    fileName = Column(String(255), nullable=True)
    moneyFormId = Column(Integer, ForeignKey('moneyForm.id'))
    comment = Column(String(255))
    userId = Column(Integer, ForeignKey('user.id'))
    createdAt = Column(TIMESTAMP, default=text("CURRENT_TIMESTAMP"))
    electrAmount = Column(Numeric, default=0)
    type = Column(Enum(IncomeType), default='rent')

    client = relationship('Client', backref='incomes')
    moneyForm = relationship('Moneyform', backref='incomes')
    user = relationship('User', backref='incomes')
