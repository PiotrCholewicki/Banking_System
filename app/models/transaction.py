from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Numeric, Column
from typing import Optional, TYPE_CHECKING

class Transaction(SQLModel, table=True):
    __tablename__ = "transaction"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id", index=True)
    transaction_type: str = Field(index=True)
    amount: Decimal = Field(sa_column=Column(Numeric(12, 2)))
    date: datetime = datetime.now()
    client: "Client" = Relationship(back_populates="transactions")


    def __str__(self) -> str:
        return (
            f"Transaction(id={self.id}, client_id={self.client_id}, "
            f"type={self.transaction_type}, amount={self.amount}, date={self.date})"
        )

    def __repr__(self) -> str:
        return self.__str__()




