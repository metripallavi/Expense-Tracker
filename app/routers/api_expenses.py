from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseRead
from app.services.expenses import create_expense, list_expenses

router = APIRouter()


@router.post("/expenses", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense_api(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    idempotency_key: str = Header(None, alias="Idempotency-Key"),
):
    if not idempotency_key or not idempotency_key.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required",
        )

    return create_expense(db, payload, idempotency_key.strip())


@router.get("/expenses", response_model=list[ExpenseRead])
def list_expense_api(
    category: str = None,
    sort: str = "date_desc",
    db: Session = Depends(get_db),
):
    return list_expenses(db, category=category, sort=sort)