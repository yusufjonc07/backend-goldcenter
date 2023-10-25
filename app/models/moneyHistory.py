from email.policy import default
from sqlalchemy import Column, Enum, Integer, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP, text
from app.schemas.enums import ExpenceTypes
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.moneyForm import * 
from app.models.branch import * 
from app.models.user import * 


class MoneyHistory(Base):
    __tablename__ = "moneyHistory"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ownerTable = Column(String, default='')
    ownerId = Column(Integer, default=0)
    value = Column(String, default='')
    moneyFormId = Column(Integer, ForeignKey('moneyForm.id'), default=0)
    floorId = Column(Integer, ForeignKey('floor.id'), default=0)
    branchId = Column(Integer, ForeignKey('branch.id'), default=0)
    comment = Column(String, default='')
    userId = Column(Integer, ForeignKey('user.id'), default=0)
    fileName = Column(Text, default='')
    createdAt = Column(TIMESTAMP, default=text("CURRENT_TIMESTAMP"))
    addingToFee = Column(Enum(ExpenceTypes), default='none')

    moneyForm = relationship('Moneyform', backref='moneyHistorys')
    branch = relationship('Branch', backref='moneyHistorys')
    user = relationship('User', backref='moneyHistorys')

