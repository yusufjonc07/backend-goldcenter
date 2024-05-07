from sqlalchemy import Column, Date, Integer, Enum, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from app.schemas.attandanceOne import AttTypeHik
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.employee import *


class Attandance(Base):
    __tablename__ = "attandance"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String)
    employeeId = Column(Integer, ForeignKey('employee.id'), default=0)
    workTime = Column(Numeric)
    authorizator = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=func.now())

    employee = relationship('Employee', backref='attandances')
