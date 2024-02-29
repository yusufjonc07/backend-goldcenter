from email.policy import default
from sqlalchemy import Column, Enum, Integer, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP, text
from app.schemas.enums import ExpenceTypes
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.moneyForm import *
from app.models.branch import *
from app.models.user import *
from app.models.employee import *
from sqlalchemy.dialects.mysql import DOUBLE


class Expense(Base):
    __tablename__ = "expense"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Enum(ExpenceTypes), default='other', nullable=False)
    employeeId = Column(Integer, ForeignKey('employee.id'), nullable=True)
    regularExpenceId = Column(Integer, ForeignKey(
        'regularExpence.id'), nullable=True)
    value = Column(DOUBLE, nullable=False)
    moneyFormId = Column(Integer, ForeignKey('moneyForm.id'), nullable=False)
    branchId = Column(Integer, ForeignKey('branch.id'), nullable=False)
    comment = Column(String(255))
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)
    fileName = Column(Text, nullable=True)
    isAvanse = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP, default=text("CURRENT_TIMESTAMP"))

    employee = relationship('Employee', backref='expenses')
    moneyForm = relationship('Moneyform', backref='expenses')
    branch = relationship('Branch', backref='expenses')
    user = relationship('User', backref='expenses')
