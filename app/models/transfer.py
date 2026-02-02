from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Numeric, Column
from sqlmodel import SQLModel, Field


class Transfer(SQLModel, table=True):
    __tablename__ = "transfer"

    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="client.id", index=True)
    receiver_id: int = Field(foreign_key="client.id", index=True)
    amount: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    date: datetime = datetime.now()
    # client: "Client" = Relationship(back_populates="transactions")

    def __str__(self) -> str:
        return (
            f"Transfer(id={self.id}, sender_id={self.sender_id}, "
            f"receiver_id={self.receiver_id}, amount={self.amount}, date={self.date})"
        )

    def __repr__(self) -> str:
        return self.__str__()
