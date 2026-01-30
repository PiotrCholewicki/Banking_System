from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.auth.auth import get_current_user, ensure_client_access, require_admin
from app.database import get_session
from app.models.client import Client
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionRead, TransactionCreate
from app.services import banking_service

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionRead)
def create_transaction(payload: TransactionCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):

    client = session.get(Client, current_user.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    ensure_client_access(client, current_user)


    transaction = banking_service.register_transaction(
        session,
        client_id=current_user.client_id,
        amount=payload.amount,
        transaction_type=payload.transaction_type
    )
    return transaction







