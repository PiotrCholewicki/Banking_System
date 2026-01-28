from decimal import Decimal
from fastapi import HTTPException
from sqlmodel import Session
from app.models.client import Client
from app.models.transaction import Transaction
from app.models.transfer import Transfer
from app.validators.value_validators import validate_transaction_type, validate_amount

def register_transfer(session: Session, sender_id: int, receiver_id: int, amount: Decimal):
    sender = session.get(Client, sender_id)
    receiver = session.get(Client, receiver_id)


    if sender_id == receiver_id:
        raise HTTPException(status_code=400, detail="Sender and receiver must be different")


    if not (sender and receiver):
        raise HTTPException(status_code=404, detail="Client not found")

    if not validate_amount(amount):
        raise HTTPException(status_code=400, detail="Amount should be positive integer or float")

    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")
    #sender transaction
    outgoing_transfer = Transaction(
        client_id=sender_id,
        transaction_type="outgoing transfer",
        amount=amount
    )
    sender.balance -= amount
    incoming_transfer = Transaction(
        client_id=receiver_id,
        transaction_type="incoming transfer",
        amount=amount
    )
    receiver.balance += amount
    transfer = Transfer(
        receiver_id=receiver_id,
        sender_id=sender_id,
        amount=amount,
    )
    session.add(outgoing_transfer)
    # session.add(sender)
    session.add(incoming_transfer)
    # session.add(receiver)
    session.add(transfer)
    session.commit()
    session.refresh(outgoing_transfer)
    session.refresh(incoming_transfer)
    session.refresh(transfer)
    # session.refresh(client)


    return transfer

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
    session.refresh(transaction)
    # session.refresh(client)
    return transaction


