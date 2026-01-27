from decimal import Decimal
from fastapi import HTTPException
from sqlmodel import Session
from app.models.client import Client
from app.models.transaction import Transaction
from app.validators.value_validators import validate_transaction_type, validate_amount


def register_transaction(session: Session, client_id: int, amount: Decimal, transaction_type: str):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if not validate_amount(amount):
        raise HTTPException(status_code=400, detail="Amount should be positive integer or float")

    if not validate_transaction_type(transaction_type):
        raise HTTPException(status_code=400, detail="Transaction type should be either withdrawal or deposit")

    if transaction_type == "withdrawal":
        if amount > client.balance: raise HTTPException(status_code=400, detail="Insufficient funds")
        client.balance -= amount

    elif transaction_type == "deposit":
        client.balance += amount

    transaction = Transaction(
        client_id=client.id,
        transaction_type=transaction_type,
        amount=amount
    )
    session.add(transaction)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


