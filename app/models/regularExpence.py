from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.floor import * 
from app.models.branch import * 


class Regularexpence(Base):
    __tablename__ = "regularExpence"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    floorId = Column(Integer, ForeignKey('floor.id'), default=0)
    branchId = Column(Integer, ForeignKey('branch.id'), default=0)
    addingToFee = Column(String, default='')

    floor = relationship('Floor', backref='regularExpences')
    branch = relationship('Branch', backref='regularExpences')

