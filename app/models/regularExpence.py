from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.floor import *
from app.models.branch import *


class RegularExpence(Base):
    __tablename__ = "regularExpence"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    balance = Column(Numeric, default=0)
