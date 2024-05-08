from enum import unique
from sqlalchemy import Column, UniqueConstraint, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from app.schemas.enums import DEPARTMENT_LABELS
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.branch import *
from app.models.shift import *
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.ext.hybrid import hybrid_method


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, default='')
    lastname = Column(String, default='')
    pnfl = Column(String, nullable=True, unique=True)
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

    @hybrid_property
    def _fullname(self):
        return func.concat(self.firstname, ' ', self.lastname)

    @hybrid_property
    def _department(self):
        return DEPARTMENT_LABELS[self.role]

    UniqueConstraint('firstname', 'lastname')

    branch = relationship('Branch', backref='employees')
    shift = relationship('Shift', backref='employees')
