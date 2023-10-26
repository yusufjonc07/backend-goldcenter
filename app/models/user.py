from enum import unique
from sqlalchemy import Column, Date, Integer, Enum, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from app.schemas.enums import UserRoles
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.branch import * 
from app.models.employee import * 


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userRole = Column(Enum(UserRoles))
    username = Column(String, unique=True)
    passwordHash = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    branchId = Column(Integer, ForeignKey('branch.id'), nullable=True)
    employeeId = Column(Integer, ForeignKey('employee.id'), default=0)

    branch = relationship('Branch', backref='users')
    employee = relationship('Employee', backref='users', lazy='joined')

