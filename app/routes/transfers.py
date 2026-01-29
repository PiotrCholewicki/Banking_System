from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session

from app.auth.auth import get_current_user
from app.database import get_session
from app.models.client import Client
from app.models.user import User

from app.schemas.transfer import TransferRead, TransferCreate
from app.services import banking_service

router = APIRouter(prefix="/transfers", tags=["transfers"])

@router.post("/", response_model=TransferRead)
def create_transfer(payload: TransferCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    sender = session.get(Client, current_user.client_id)
    receiver = session.get(Client, payload.receiver_id)
    if not (sender and receiver):
        raise HTTPException(status_code=404, detail="Client not found")

    transfer = banking_service.register_transfer(
        session,
        receiver_id=payload.receiver_id,
        sender_id=current_user.client_id,
        amount=payload.amount,
    )
    return transfer