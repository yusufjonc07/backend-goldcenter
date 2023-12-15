from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, select, literal_column, text
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

class Shift(Base):
    __tablename__ = "shift"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')
    workBeginTime = Column(Time, nullable=True)
    workEndTime = Column(Time, nullable=True)