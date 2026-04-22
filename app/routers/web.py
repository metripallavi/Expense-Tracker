from decimal import Decimal

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.expense import Expense
from app.services.expenses import list_expenses

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def calculate_total(expenses: list[Expense]) -> Decimal:
    total = Decimal("0.00")
    for expense in expenses:
        total += Decimal(str(expense.amount))
    return total


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    category: str = None,
    sort: str = "date_desc",
    db: Session = Depends(get_db),
):
    expenses = list_expenses(db=db, category=category, sort=sort)
    total = calculate_total(expenses)

    categories = [
        row[0]
        for row in db.query(Expense.category).distinct().order_by(Expense.category.asc()).all()
    ]

    context = {
        "request": request,
        "expenses": expenses,
        "total": total,
        "selected_category": category or "",
        "selected_sort": sort,
        "categories": categories,
    }

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )