from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref


class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fileName = Column(Text, default='')
    createdAt = Column(DateTime, nullable=True)


