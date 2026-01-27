from decimal import Decimal
from sqlalchemy import Numeric, Column
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.transaction import Transaction

class Client(SQLModel, table=True):
    __tablename__ = "client"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    balance: Decimal = Field(
        default=Decimal("0.00"),
        sa_column=Column(Numeric(12, 2))
    )

    transactions: List["Transaction"] = Relationship(back_populates="client")

    #explicit return type declaration with ->
    def __str__(self) -> str:
        return f"Client(id={self.id}, name={self.name}, balance={self.balance})"

    def __repr__(self) -> str:
        return self.__str__()






