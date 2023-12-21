from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref


class Branch(Base):
    __tablename__ = "branch"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    address = Column(String, default='')
    dollar = Column(Numeric)
