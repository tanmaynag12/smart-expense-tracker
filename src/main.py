from fastapi import FastAPI, HTTPException
from src.models import ExpenseCreate, Expense
from src import storage

app = FastAPI(title="Smart Expense Tracker API")


@app.post("/expenses", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseCreate):
    return storage.add_expense(expense.model_dump(mode="json"))


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: str | None = None):
    if category:
        return storage.get_by_category(category)
    return storage.get_all()


@app.get("/expenses/total")
def total_expenses():
    return storage.get_totals()


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    deleted = storage.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")