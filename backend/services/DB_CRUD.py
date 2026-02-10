from sqlalchemy.orm import sessionmaker
from backend.utils.data_models import Expense
from backend.services.DB_Create import engine
from uuid import UUID

Session = sessionmaker(bind=engine)

# Create a new session for each operation
def get_session():
    return Session()

# Create
def create_expense(name, amount, date, inflow, tags=None, remarks=None):
    session = get_session()
    try:
        new_expense = Expense(name=name, amount=amount, inflow=inflow, date=date, tags=tags, remarks=remarks)
        session.add(new_expense)
        session.commit()
        return new_expense
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Read
def get_expenses():
    session = get_session()
    try:
        return session.query(Expense).all()
    finally:
        session.close()

def get_expense_by_id(expense_id):
    session = get_session()
    try:
        expense_id = UUID(expense_id)
        return session.query(Expense).filter(Expense.id == expense_id).first()
    finally:
        session.close()

# Update
def update_expense(expense_id, name=None, amount=None, date=None, inflow=None):
    session = get_session()
    try:
        expense_id = UUID(expense_id)
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            if name:
                expense.name = name
            if amount:
                expense.amount = amount
            if date:
                expense.date = date
            if inflow:
                expense.inflow = inflow
            session.commit()
        return expense
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Delete
def delete_expense(expense_id):
    session = get_session()
    try:
        expense_id = UUID(expense_id)
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            session.delete(expense)
            session.commit()
        return expense
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()