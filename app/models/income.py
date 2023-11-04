from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func, TIMESTAMP
from databases.main import Base
from sqlalchemy.orm import relationship, backref
from app.models.clientAgreement import * 
from app.models.moneyForm import * 
from app.models.user import * 


class Income(Base):
    __tablename__ = "income"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, default='')
    clientAgreementId = Column(Integer, ForeignKey('clientAgreement.id'), default=0)
    value = Column(Numeric, default=0)
    moneyFormId = Column(Integer, ForeignKey('moneyForm.id'), default=0)
    comment = Column(String, default='')
    userId = Column(Integer, ForeignKey('user.id'), default=0)
    createdAt = Column(TIMESTAMP, nullable=True)

    clientAgreement = relationship('Clientagreement', backref='incomes')
    moneyForm = relationship('Moneyform', backref='incomes')
    user = relationship('User', backref='incomes')

