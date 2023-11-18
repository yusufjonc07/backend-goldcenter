from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from databases.main import Base
from sqlalchemy.orm import relationship
from app.models.branch import * 


class ParkingZone(Base):
    __tablename__ = "parkingZone"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    hourlyFee = Column(Numeric)
    branchId = Column(Integer, ForeignKey('branch.id'))

    branch = relationship('Branch', backref='parkingZones')

