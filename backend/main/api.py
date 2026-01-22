from fastapi import FastAPI
from backend.services.DB_CRUD import create_expense, delete_expense


app = FastAPI()

@app.post('/insert-expense/{expense_id}')
async def insert_expense(expense_id:str, amount:float, tags:str):
    print(expense_id)