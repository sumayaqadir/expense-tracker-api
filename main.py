from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI(title="Smart Expense Tracker API")

# ---- In-memory storage ----
expenses: list[dict] = []


# ---- Data model for creating an expense ----
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    date: str  # expected format: YYYY-MM-DD


class Expense(ExpenseCreate):
    id: str


# ---- 1. Add an expense ----
@app.post("/expenses", response_model=Expense)
def add_expense(expense: ExpenseCreate):
    new_expense = expense.model_dump()
    new_expense["id"] = str(uuid4())
    expenses.append(new_expense)
    return new_expense


# ---- 2. View all expenses ----
@app.get("/expenses", response_model=list[Expense])
def get_expenses():
    return expenses


# ---- 3. Filter expenses by category ----
@app.get("/expenses/category/{category}", response_model=list[Expense])
def get_expenses_by_category(category: str):
    filtered = [e for e in expenses if e["category"].lower() == category.lower()]
    return filtered


# ---- 4. Calculate totals (overall and by category) ----
@app.get("/expenses/total")
def get_totals(category: Optional[str] = None):
    if category:
        matched = [e for e in expenses if e["category"].lower() == category.lower()]
        total = sum(e["amount"] for e in matched)
        return {"category": category, "total": total}

    overall_total = sum(e["amount"] for e in expenses)
    by_category: dict[str, float] = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    return {"overall_total": overall_total, "by_category": by_category}


# ---- 5. Delete an expense ----
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            expenses.pop(i)
            return {"message": "Expense deleted", "id": expense_id}
    raise HTTPException(status_code=404, detail="Expense not found")
