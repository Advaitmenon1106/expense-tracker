from sqlalchemy import Column, Integer, String, Float, Date, Boolean, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expense'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    inflow = Column(Boolean, nullable=False)
    date = Column(Date, nullable=False)
    tags = Column(String, nullable=True)  # Optional field for tags
    remarks = Column(String, nullable=True)  # Optional field for remarks