from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, default='')
    lastname = Column(String, default='')
    phoneNumber = Column(Integer, default=0)
    passportSeriaNumber = Column(String, default='')
    inn = Column(String, default='')


