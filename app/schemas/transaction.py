from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel


class TransactionCreate(SQLModel):
    transaction_type: str
    amount: Decimal
    # client_id: int


class TransactionRead(SQLModel):
    id: int
    transaction_type: str
    amount: Decimal
    client_id: int
    date: datetime


class TransactionReadNoId(SQLModel):
    # id: int
    transaction_type: str
    amount: Decimal
    date: datetime
