from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref


class Moneyform(Base):
    __tablename__ = "moneyForm"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, default='')


