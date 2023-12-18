from sqlalchemy import Column, Enum, Integer, func, String, ForeignKey, and_
from app.schemas.enums import ChatTypes, TaskTypes
from databases.main import Base
from sqlalchemy.orm import relationship
from app.models.user import *
from app.models.branch import *

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    context = Column(String, default=False)
    fileName = Column(Text, default=False)
    employeeId = Column(Integer, default=False)
    forRole = Column(Enum(ChatTypes), default=False)
    branchId = Column(Integer, ForeignKey('branch.id'), default=False)
    createdAt = Column(DateTime, nullable=False, default=func.now())

    completedAt = Column(DateTime, nullable=True)
    responseText =  Column(String, nullable=True)
    responseType = Column(Enum(TaskTypes), nullable=True)
    responseFileName = Column(Text, nullable=False)
    responseEmployeeId = Column(Integer, nullable=False)

    employee = relationship('Employee', foreign_keys=[employeeId], primaryjoin=lambda: and_(Employee.id == Task.employeeId))
    responseEmployee = relationship('Employee', foreign_keys=[responseEmployeeId], primaryjoin=lambda: and_(Employee.id == Task.responseEmployeeId))
    branch = relationship('Branch', backref='messages')

   
    
