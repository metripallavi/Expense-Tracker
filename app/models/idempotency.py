from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    __table_args__ = (UniqueConstraint("key", name="uq_idempotency_key"),)

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), nullable=False, index=True)
    request_hash = Column(String(64), nullable=False)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    expense = relationship("Expense")