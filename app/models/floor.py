from sqlalchemy import Column, Enum, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from app.schemas.enums import FloorTypes
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.branch import *


class Floor(Base):
    __tablename__ = "floor"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    number = Column(Integer, default=0)
    description = Column(String, default='')
    coridorCleaningCost = Column(String, default='')
    branchId = Column(Integer, ForeignKey('branch.id'), nullable=True)
    type = Column(Enum(FloorTypes))

    branch = relationship('Branch', backref='floors')
