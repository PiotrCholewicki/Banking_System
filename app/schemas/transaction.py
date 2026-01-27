from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel


class TransactionCreate(SQLModel):
    transaction_type: str
    amount: Decimal
    client_id: int

class TransactionUpdate(SQLModel):
    transaction_type: Optional[str] = None
    amount: Optional[Decimal] = None


class TransactionRead(SQLModel):
    id: int
    transaction_type: str
    amount: Decimal
    client_id: int
    date: datetime