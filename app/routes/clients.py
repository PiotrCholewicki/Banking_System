from decimal import Decimal
from http.client import responses
import app.services.banking_service as banking_service
from fastapi.params import Depends
from sqlalchemy import Column, Numeric
from sqlmodel import Session, select, Field
from fastapi import Response, APIRouter, HTTPException
from app.database import get_session
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate, ClientReadWithTransactions
from app.models.client import Client
from app.validators.value_validators import validate_client_name, validate_amount, validate_client_id, \
    validate_transaction_type

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientRead)
def create_client(payload: ClientCreate, session: Session = Depends(get_session)):
    if validate_client_name(payload.name) and validate_amount(payload.balance):
        client = Client(
            name=payload.name,
            balance=payload.balance,
        )
        session.add(client)
        session.commit()
        session.refresh(client)
        return client
    else:
        raise HTTPException(status_code=404, detail="Validation Error")

@router.get("/{client_id}", response_model=ClientReadWithTransactions)
def get_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/", response_model=list[ClientRead])
def list_clients(session: Session = Depends(get_session)):
    return session.exec(select(Client)).all()

@router.delete("/{client_id}", status_code=204)
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

# @router.post("/{client_id}/{amount}/{transaction_type}", response_model=ClientRead)
# def register_transaction(client_id: int, amount: Decimal, transaction_type: str, session: Session = Depends(get_session)):
#     if validate_client_id(client_id) and validate_amount(amount) and validate_transaction_type(transaction_type):
#         updated = banking_service.register_transaction(session, client_id, amount, transaction_type)
#         return updated
#     else: raise HTTPException(status_code=400, detail="Validation error")

