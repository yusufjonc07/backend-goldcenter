from sqlalchemy import Column, Integer, String
from databases.main import Base

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    clientName = Column(String, unique=True)
    chiefName = Column(String, unique=True)
    phoneNumber = Column(Integer)
    inn = Column(String(20))
    extraPhoneNumber = Column(Integer, nullable=True)


