from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models.transaction import Transaction
from app.models.user import User
from app.models.client import Client
from app.auth.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, require_admin,
)
from app.routes.clients import delete_client
from app.schemas.auth import UserRegister, Token
from app.schemas.client import ClientReadWithTransactions
from app.schemas.transaction import TransactionRead

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/clients/", response_model=list[ClientReadWithTransactions])
def list_clients(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    return session.exec(select(Client)).all()

@router.get("/users/")
def list_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    require_admin(current_user)
    return session.exec(select(User)).all()

@router.get("/transactions", response_model=list[TransactionRead])
def list_transactions(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # admin = session.get(Client, admin.client_id) - only for admin
    # ensure_client_access(client, current_user)
    require_admin(current_user)
    return session.exec(select(Transaction)).all()

@router.get("/clients/{client_id}", response_model=ClientReadWithTransactions)
def get_client_with_provided_id(
    client_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    client = session.get(Client, client_id)
    require_admin(current_user)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_username(username: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):

    require_admin(current_user)
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Can't delete admin")

    if user.client_id:
        delete_client(user.client_id, session)

    session.delete(user)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)