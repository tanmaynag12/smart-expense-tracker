import json
from pathlib import Path
from src.models import Expense

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.json"


def load() -> list[dict]:
    """Read all expenses from the JSON file. Returns [] if the file doesn't exist yet."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save(expenses: list[dict]) -> None:
    """Write the given list of expenses back to the JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2, default=str)


def get_all() -> list[dict]:
    return load()


def get_by_category(category: str) -> list[dict]:
    expenses = load()
    return [e for e in expenses if e["category"].lower() == category.lower()]


def add_expense(expense_data: dict) -> dict:
    """Assign the next id, store the expense, and return it (as a dict)."""
    expenses = load()
    next_id = max((e["id"] for e in expenses), default=0) + 1
    new_expense = Expense(id=next_id, **expense_data)
    expense_dict = new_expense.model_dump(mode="json")
    expenses.append(expense_dict)
    save(expenses)
    return expense_dict


def delete_expense(expense_id: int) -> bool:
    """Delete by id. Returns True if something was deleted, False if id not found."""
    expenses = load()
    filtered = [e for e in expenses if e["id"] != expense_id]
    if len(filtered) == len(expenses):
        return False
    save(filtered)
    return True


def get_totals() -> dict:
    expenses = load()
    overall_total = sum(e["amount"] for e in expenses)
    by_category: dict[str, float] = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]
    return {"overall_total": overall_total, "by_category": by_category}