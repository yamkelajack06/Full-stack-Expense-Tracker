from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.tracker import Expense_Tracker
from datetime import datetime as dt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

expense_tracker = Expense_Tracker()


class ExpenseRequest(BaseModel):
    name: str
    amount: float
    category: str


class UpdateExpenseRequest(BaseModel):
    name: str | None = None
    amount: float | None = None
    category: str | None = None


@app.get("/")
def root():
    return {"message": "Expense Tracker API is running 💰"}


@app.get("/expenses/search")
def search_expenses(q: str):
    results = expense_tracker.search_expense(q)
    if not results:
        return {"expenses": [], "message": "No expenses found"}
    return {"expenses": [e.to_dict() for e in results]}


@app.get("/expenses/summary")
def get_summary():
    expense_tracker.organize_expenses()
    return expense_tracker.display_spending_summary()


@app.get("/expenses/filter")
def filter_expenses(
    category: str | None = None,
    month: int | None = None,
    year: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):
    if category:
        results = expense_tracker.filter_by_category(category)
    elif month and year:
        results = expense_tracker.filter_by_month_and_year({"month": month, "year": year})
    elif start_date and end_date:
        start = dt.strptime(start_date, "%Y-%m-%d")
        end = dt.strptime(end_date, "%Y-%m-%d")
        results = expense_tracker.filter_by_date_range(start, end)
    else:
        raise HTTPException(status_code=400, detail="Provide a filter: category, month+year, or start_date+end_date")

    if not results:
        return {"expenses": [], "message": "No expenses match that filter"}
    return {"expenses": [e.to_dict() for e in results]}


@app.get("/expenses")
def get_expenses():
    if not expense_tracker.expenses:
        return {"expenses": [], "message": "No expenses found"}
    return {"expenses": [e.to_dict() for e in expense_tracker.expenses]}


@app.post("/expenses")
def add_expense(expense: ExpenseRequest):
    expense_tracker.add_expense(expense.name, expense.amount, expense.category)
    return {"message": "Expense added successfully", "expense": expense.model_dump()}


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    target = next((e for e in expense_tracker.expenses if str(e.id) == expense_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense_tracker.delete_expense(target)
    return {"message": f"Expense '{target.name}' deleted successfully"}


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: str, fields: UpdateExpenseRequest):
    target = next((e for e in expense_tracker.expenses if str(e.id) == expense_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Expense not found")
    fields_to_update = {k: v for k, v in fields.model_dump().items() if v is not None}
    expense_tracker.update_expenses(target, fields_to_update)
    return {"message": "Expense updated successfully"}