from decimal import Decimal
from typing import Optional, List
from sqlmodel import SQLModel


class ClientCreate(SQLModel):
    name: str
    balance: Decimal


class ClientUpdate(SQLModel):
    name: Optional[str] = None
    balance: Optional[Decimal] = None


class ClientRead(SQLModel):
    id: int
    name: str
    balance: Decimal


from app.schemas.transaction import TransactionRead


class ClientReadWithTransactions(ClientRead):
    transactions: List[TransactionRead] = []
