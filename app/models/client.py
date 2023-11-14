from sqlalchemy import Column, Enum, Integer, Text, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from app.schemas.enums import AgreementStatus, AgreementType
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.shop import * 


class Client(Base):
    __tablename__ = "client"
    clientName = Column(String, unique=True)
    chiefName = Column(String, unique=True)
    phoneNumber = Column(Integer)
    inn = Column(String(20))
    extraPhoneNumber = Column(Integer, nullable=True)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fileName = Column(Text, nullable=False)
    liablePerson = Column(String(255))
    shopId = Column(Integer, ForeignKey('shop.id'), default=0)
    clientId = Column(Integer, ForeignKey('client.id'), default=0)
    monthlyFee = Column(DOUBLE, default=0)
    balance = Column(DOUBLE, default=0)
    status = Column(Enum(AgreementStatus), default='active')
    type = Column(Enum(AgreementType))
    startedAt = Column(Date)
    closedAt = Column(Date, nullable=True)

    UniqueConstraint("clientId", "shopId", "status")

    shop = relationship('Shop', backref=backref('clientAgreement', uselist=False))
    client = relationship('Client', backref='clientAgreements')

