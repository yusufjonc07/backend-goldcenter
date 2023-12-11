from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.employee import * 


class Salary(Base):
    __tablename__ = "salary"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employeeId = Column(Integer, ForeignKey('employee.id'), default=0)
    calcWage = Column(Numeric, default=0)
    isConfirmed = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=func.now())

    employee = relationship('Employee', backref='salarys', lazy='joined')

