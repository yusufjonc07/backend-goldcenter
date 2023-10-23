from sqlalchemy import Column, Double, Enum, Integer, Text, ForeignKey
from app.schemas.enums import AgreementStatus, AgreementType
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.shop import * 
from app.models.client import * 


class ClientAgreement(Base):
    __tablename__ = "clientAgreement"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fileName = Column(Text, default='')
    shopId = Column(Integer, ForeignKey('shop.id'), default=0)
    clientId = Column(Integer, ForeignKey('client.id'), default=0)
    monthlyFee = Column(Double, default=0)
    balance = Column(Double, default=0)
    status = Column(Enum(AgreementStatus), default='active')
    type = Column(Enum(AgreementType))
    startedAt = Column(Date)
    closedAt = Column(Date, nullable=True)

    shop = relationship('Shop', backref='clientAgreements')
    client = relationship('Client', backref='clientAgreements')

