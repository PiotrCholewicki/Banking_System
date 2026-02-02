from typing import Optional

from sqlmodel import SQLModel


class UserRead(SQLModel):
    username: str
    hashed_password: str
    role: str
    is_active: bool
    client_id: Optional[int]
