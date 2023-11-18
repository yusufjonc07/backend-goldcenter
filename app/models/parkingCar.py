from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.parkingZone import * 


class ParkingCar(Base):
    __tablename__ = "parkingCar"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(String, default='')
    hourlyFee = Column(Numeric, default=0)
    totalFee = Column(Numeric, default=0)
    parkingZoneId = Column(Integer, ForeignKey('parkingZone.id'), nullable=True)
    enteredAt = Column(TIMESTAMP, nullable=True)
    exitedAt = Column(TIMESTAMP, nullable=True)

    parkingZone = relationship('ParkingZone', backref='parkingCars')

