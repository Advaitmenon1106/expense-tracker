from fastapi import FastAPI
from backend.services.DB_CRUD import create_expense, delete_expense, update_expense, get_expenses, get_expense_by_id
from datetime import date as DateType
from uuid import UUID

app = FastAPI()

@app.post('/insert-expense')
async def insert_expense(expense_name: str, amount: float, date: DateType, inflow:bool, tags: str = None, remarks: str = None):
    return create_expense(name=expense_name, amount=amount, date=date, tags=tags, remarks=remarks, inflow=inflow)


@app.get('/retrieve-all-expenses')
async def retrieve_all_expenses():
    return get_expenses()


@app.get('/retrieve-expense/{expense_id}')
async def retrieve_expense(expense_id):
    return get_expense_by_id(expense_id=expense_id)


@app.delete('delete/{expense_id}')
async def delete_expense(expense_id):
    return delete_expense(expense_id=expense_id)