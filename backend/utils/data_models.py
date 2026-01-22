from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)