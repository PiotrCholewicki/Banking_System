import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pwdlib import PasswordHash
from sqlmodel import Session, select

from app.database import get_session
from app.models.client import Client
from app.models.user import User

# to get a string like this run:
# openssl rand -hex 32


JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user_by_username(session: Session, username):
    return session.exec(select(User).where(User.username == username)).first()



def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user



def create_access_token(data: dict, expires_delta: timedelta, role: str | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire, "role": role})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exc

    except (InvalidTokenError, ExpiredSignatureError):
        raise credentials_exc

    # sub is user_id (string → int)
    try:
        user_id = int(sub)
        user = session.get(User, user_id)
    except ValueError:

        user = get_user_by_username(session, sub)

    if not user:
        raise credentials_exc
    return user



async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")

def ensure_client_access(client: Client, current_user: User):
    # jeśli user ma rolę admin → full access
    if current_user.role == "admin":
        return

    # jeśli user ma rolę client → tylko własny klient
    if current_user.role == "client" and current_user.client_id == client.id:
        return

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

