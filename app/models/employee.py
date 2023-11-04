from enum import unique
from sqlalchemy import Column, UniqueConstraint, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.branch import * 
from app.models.shift import * 
from sqlalchemy.dialects.mysql import DOUBLE

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, default='')
    lastname = Column(String, default='')
    phoneNumber = Column(Integer, default=0)
    balance = Column(Numeric, default=0)
    passportFile = Column(Text)
    agreementFile = Column(Text)
    birthDate = Column(Date)
    avatarFile = Column(Text, default='')
    salaryQuantity = Column(String, default='')
    role = Column(String, default='')
    duty = Column(String, default='')
    fired = Column(Boolean, default=False)
    branchId = Column(Integer, ForeignKey('branch.id'), nullable=True)
    shiftId = Column(Integer, ForeignKey('shift.id'), default=0)

    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    UniqueConstraint('firstname', 'lastname')
    
    branch = relationship('Branch', backref='employees')
    shift = relationship('Shift', backref='employees')

