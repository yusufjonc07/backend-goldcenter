from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, UniqueConstraint, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.floor import *
from sqlalchemy.dialects.mysql import DOUBLE


class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    number = Column(String, default='')
    floorId = Column(Integer, ForeignKey('floor.id'))
    clientId = Column(Integer, nullable=True)
    area = Column(Numeric, default=0)
    fromTop = Column(Numeric, default=0)
    fromLeft = Column(Numeric, default=0)
    boxWith = Column(Numeric, default=0)
    boxHeight = Column(Numeric, default=0)
    deleted = Column(Boolean, default=False)

    UniqueConstraint("number", "floorId")

    floor = relationship('Floor', backref='shops')
