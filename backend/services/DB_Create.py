from sqlalchemy import create_engine
from backend.utils.data_models import Base
from dotenv import load_dotenv
import os

load_dotenv()

username=os.environ['POSTGRES_USERNAME']
password = os.environ['POSTGRES_PASSWORD']

DATABASE_URL = f"postgresql://{username}:{password}@localhost:5432/expense_db"

engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)