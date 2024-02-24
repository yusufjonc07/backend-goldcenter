from sqlalchemy import Column, Integer, Numeric, String
from databases.main import Base


class Moneyform(Base):
    __tablename__ = "moneyForm"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    balance = Column(Numeric, default=0)
