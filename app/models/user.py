from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str  # user / admin
    is_active: bool = Field(default=True)
    client_id: Optional[int] = Field(foreign_key="client.id", unique=True)
