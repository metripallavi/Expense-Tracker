from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.expense import Expense
from app.models.idempotency import IdempotencyKey
from app.utils.hashing import build_request_hash


def create_expense(db: Session, payload, key: str):
    payload_dict = payload.model_dump()

    payload_for_hash = {
        **payload_dict,
        "date": str(payload_dict["date"]),
        "amount": str(payload_dict["amount"]),
    }
    request_hash = build_request_hash(payload_for_hash)

    try:
        # ✅ Create expense first
        expense = Expense(**payload_dict)
        db.add(expense)
        db.flush()  # ensures expense.id is available

        # ✅ Insert idempotency key (atomic via DB constraint)
        idem = IdempotencyKey(
            key=key,
            request_hash=request_hash,
            expense_id=expense.id,
        )
        db.add(idem)

        # ✅ Commit both together
        db.commit()
        db.refresh(expense)

        return expense

    except IntegrityError:
        # 🔥 Handles race condition safely
        db.rollback()

        existing = db.query(IdempotencyKey).filter_by(key=key).first()

        if not existing:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Race condition fallback failed",
            )

        if existing.request_hash != request_hash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency key already used with different payload",
            )

        return existing.expense


def list_expenses(db: Session, category=None, sort="date_desc"):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category.strip())

    if sort == "date_desc":
        query = query.order_by(
            Expense.date.desc(),
            Expense.created_at.desc(),
            Expense.id.desc(),
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported sort value. Supported value: date_desc",
        )

    return query.all()