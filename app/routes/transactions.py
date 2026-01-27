from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.client import Client
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionRead, TransactionCreate
from app.services import banking_service

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionRead)
def create_transaction(payload: TransactionCreate, session: Session = Depends(get_session)):

    client = session.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    transaction = banking_service.register_transaction(
        session,
        client_id=payload.client_id,
        amount=payload.amount,
        transaction_type=payload.transaction_type
    )
    return transaction


@router.get("/", response_model=list[TransactionRead])
def list_transactions(session: Session = Depends(get_session)):
    return session.exec(select(Transaction)).all()



