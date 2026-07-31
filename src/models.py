from pydantic import BaseModel, Field, field_validator
from datetime import date as date_type


class ExpenseCreate(BaseModel):
    """What the client sends when creating an expense — no id, they don't set that."""
    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    date: date_type

    @field_validator("title", "category")
    @classmethod
    def strip_and_check_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank or whitespace only")
        return v


class Expense(ExpenseCreate):
    """What gets stored and returned — adds the server-generated id."""
    id: int