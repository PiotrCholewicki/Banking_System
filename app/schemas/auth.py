from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str
    role: Optional[str] = None

class UserRegister(SQLModel):
    username: str
    password: str
    # role: str  # "admin" | "client"