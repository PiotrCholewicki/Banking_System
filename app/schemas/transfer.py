from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel


class TransferCreate(SQLModel):

    receiver_id: int
    amount: Decimal


class TransferRead(SQLModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: Decimal
    date: datetime