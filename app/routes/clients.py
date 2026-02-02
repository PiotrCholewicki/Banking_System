from decimal import Decimal
from http.client import responses
from typing import List

from fastapi_pagination import Page, paginate

import app.services.banking_service as banking_service
from fastapi.params import Depends
from sqlalchemy import Column, Numeric
from sqlmodel import Session, select, Field
from fastapi import Response, APIRouter, HTTPException

from app.auth.auth import get_current_user, require_admin, ensure_client_access
from app.database import get_session
from app.models.user import User
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate, ClientReadWithTransactions
from app.models.client import Client
from app.schemas.transaction import TransactionRead, TransactionReadNoId
from app.validators.value_validators import validate_client_name, validate_amount, validate_client_id, \
    validate_transaction_type

router = APIRouter(prefix="/clients", tags=["clients"])


def create_client(payload: ClientCreate, session: Session = Depends(get_session)):
    client = Client(
        name=payload.name,
        balance=payload.balance,
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.get("/me/", response_model=ClientRead)
def get_my_info(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):

    client = session.get(Client, current_user.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")


    return client




@router.get("/me/transactions")
def get_my_transactions(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)) -> Page[TransactionReadNoId]:

    client = session.get(Client, current_user.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")


    return paginate(client.transactions)


# @router.get("/", response_model=list[ClientReadWithTransactions])
# def list_clients(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
#     require_admin(current_user)
#     return session.exec(select(Client)).all()

# @router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client or not validate_client_id:
        raise HTTPException(status_code=404, detail="Client not found")

    #cascade delete all users transactions
    for tx in client.transactions:
        session.delete(tx)
    session.delete(client)
    session.commit()
    return Response(status_code=204)



