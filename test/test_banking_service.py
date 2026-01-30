import pytest
from decimal import Decimal
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.client import Client
from app.models.transaction import Transaction
from app.services.banking_service import register_transaction


def test_register_transaction_deposit(session: Session):
    client = Client(name="Adam", balance=Decimal("100.00"))
    session.add(client)
    session.commit()

    tx = register_transaction(
        session=session,
        client_id=client.id,
        amount=Decimal("50.00"),
        transaction_type="deposit"
    )

    assert tx.client_id == client.id
    assert tx.transaction_type == "deposit"
    assert tx.amount == 50
    assert session.get(Client, client.id).balance == Decimal("150.00")


def test_register_transaction_withdrawal(session: Session):
    client = Client(name="Ewa", balance=Decimal("200.00"))
    session.add(client)
    session.commit()

    tx = register_transaction(
        session=session,
        client_id=client.id,
        amount=Decimal("80.00"),
        transaction_type="withdrawal"
    )

    assert tx.transaction_type == "withdrawal"
    assert session.get(Client, client.id).balance == Decimal("120.00")


def test_register_transaction_insufficient_funds(session: Session):
    client = Client(name="Piotr", balance=Decimal("30.00"))
    session.add(client)
    session.commit()

    with pytest.raises(HTTPException) as e:
        register_transaction(
            session=session,
            client_id=client.id,
            amount=Decimal("100.00"),
            transaction_type="withdrawal"
        )

    assert e.value.status_code == 400
    assert "Insufficient funds" in e.value.detail


def test_register_transaction_invalid_amount(session: Session):
    client = Client(name="John", balance=Decimal("100.00"))
    session.add(client)
    session.commit()

    with pytest.raises(HTTPException):
        register_transaction(
            session=session,
            client_id=client.id,
            amount=Decimal("-5"),
            transaction_type="deposit"
        )


def test_register_transaction_invalid_type(session: Session):
    client = Client(name="Ala", balance=Decimal("100.00"))
    session.add(client)
    session.commit()

    with pytest.raises(HTTPException):
        register_transaction(
            session=session,
            client_id=client.id,
            amount=Decimal("10"),
            transaction_type="NOT_A_TYPE"
        )


def test_register_transaction_client_not_found(session: Session):
    with pytest.raises(HTTPException) as e:
        register_transaction(
            session=session,
            client_id=999,
            amount=Decimal("10"),
            transaction_type="deposit"
        )

    assert e.value.status_code == 404

import pytest
from decimal import Decimal
from fastapi import HTTPException
from app.services.banking_service import register_transfer
from app.models.client import Client
from app.models.transaction import Transaction
from app.models.transfer import Transfer


def test_register_transfer_success(session):
    sender = Client(name="Adam", balance=Decimal("300.00"))
    receiver = Client(name="Ewa", balance=Decimal("200.00"))

    session.add(sender)
    session.add(receiver)
    session.commit()

    transfer = register_transfer(
        session=session,
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=Decimal("100.00")
    )

    updated_sender = session.get(Client, sender.id)
    updated_receiver = session.get(Client, receiver.id)

    assert transfer.amount == 100
    assert updated_sender.balance == Decimal("200.00")
    assert updated_receiver.balance == Decimal("300.00")

    # outgoing + incoming transactions created
    tx = session.exec(
        select(Transaction).where(Transaction.client_id == sender.id)
    ).first()
    assert tx.transaction_type == "outgoing transfer"


def test_register_transfer_same_sender_receiver(session):
    client = Client(name="Same", balance=Decimal("500.00"))
    session.add(client)
    session.commit()

    with pytest.raises(HTTPException) as e:
        register_transfer(
            session=session,
            sender_id=client.id,
            receiver_id=client.id,
            amount=Decimal("50")
        )

    assert e.value.status_code == 400
    assert "must be different" in e.value.detail


def test_register_transfer_client_not_found(session):
    sender = Client(name="Adam", balance=Decimal("100"))
    session.add(sender)
    session.commit()

    with pytest.raises(HTTPException) as e:
        register_transfer(
            session=session,
            sender_id=sender.id,
            receiver_id=999,
            amount=Decimal("10")
        )

    assert e.value.status_code == 404


def test_register_transfer_invalid_amount(session):
    sender = Client(name="A", balance=Decimal("100"))
    receiver = Client(name="B", balance=Decimal("100"))
    session.add(sender)
    session.add(receiver)
    session.commit()

    with pytest.raises(HTTPException):
        register_transfer(
            session=session,
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=Decimal("-1")
        )


def test_register_transfer_insufficient_funds(session):
    sender = Client(name="Poor", balance=Decimal("10"))
    receiver = Client(name="Rich", balance=Decimal("100"))
    session.add(sender)
    session.add(receiver)
    session.commit()

    with pytest.raises(HTTPException):
        register_transfer(
            session=session,
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=Decimal("200")
        )