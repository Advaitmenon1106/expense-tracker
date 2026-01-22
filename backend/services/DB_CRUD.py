from sqlalchemy.orm import sessionmaker
from backend.utils.data_models import Expense
from backend.services.DB_Create import engine

Session = sessionmaker(bind=engine)
session = Session()

# Create
def create_expense(name, amount, date):
    new_expense = Expense(name=name, amount=amount, date=date)
    session.add(new_expense)
    session.commit()
    return new_expense

# Read
def get_expenses():
    return session.query(Expense).all()

def get_expense_by_id(expense_id):
    return session.query(Expense).filter(Expense.id == expense_id).first()

# Update
def update_expense(expense_id, name=None, amount=None, date=None):
    expense = session.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        if name:
            expense.name = name
        if amount:
            expense.amount = amount
        if date:
            expense.date = date
        session.commit()
    return expense

# Delete
def delete_expense(expense_id):
    expense = session.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()
    return expense