from decimal import Decimal
from typing import Callable

import pytest
from click import clear
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models.client import Client


@pytest.fixture
def make_client(session: Session) -> Callable[[str, Decimal], Client]:
    def _make_client(name: str = "Adam", balance: Decimal = Decimal("300.00")) -> Client:
        c = Client(name=name, balance=balance)
        session.add(c)
        session.commit()   #
        session.refresh(c)
        return c
    return _make_client



def test_create_and_get_client(client):
    response = client.post(
        "/clients/", json={"name": "Remigiusz Cholewicki", "balance": float(200)}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] is not None
    assert data["name"] == "Remigiusz Cholewicki"
    assert data["balance"] == "200.00"


def test_create_client_no_balance(client):
    response = client.post("/clients/", json={"name": "Piotr Ch"})
    assert response.status_code == 422

def test_create_client_no_name(client):
    response = client.post("/clients/", json={"balance": 200})
    assert response.status_code == 422

def test_read_clients(session: Session, client: TestClient):
    client_1 = Client(
        name="Maks",
        balance= Decimal("300.00"))
    client_2 = Client(
        name="Jan",
        balance= Decimal("200.00"))
    session.add(client_1)
    session.add(client_2)
    session.commit()

    response = client.get("/clients/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == client_1.name
    assert data[0]["id"] == client_1.id
    assert data[1]["name"] == client_2.name
    assert data[1]["id"] == client_2.id
    assert Decimal(data[0]["balance"]) == client_1.balance
    assert Decimal(data[1]["balance"]) == client_2.balance

def test_delete_client(session: Session, client: TestClient, make_client):
    # client_1 = Client(name="Adam", balance=Decimal("300.00"))
    # session.add(client_1)
    # session.commit()

    sample_client = make_client(name="Adam", balance=Decimal("300.00"))

    response = client.delete(f"/clients/{sample_client.id}")
    client_in_db = session.get(Client, sample_client.id)
    assert response.status_code == 204
    assert client_in_db is None

def test_client_withdrawal_correct(session: Session, client: TestClient, make_client):
    client_1 = make_client()
    amount = 200
    client.post("/transactions/", json={"transaction_type": "withdrawal", "amount": amount, "client_id": client_1.id})
    response2 = client.get(f"/clients/{client_1.id}")
    data2 = response2.json()

    assert data2["balance"] == "100.00"
    assert response2.status_code == 200

def test_client_withdrawal_incorrect(session: Session, client: TestClient, make_client):
    client_1 = make_client()
    amount = 400
    response = client.post("/transactions/", json={"transaction_type": "withdrawal", "amount": amount, "client_id": client_1.id})
    assert response.status_code == 400

def test_client_deposit_correct(session: Session, client: TestClient, make_client):
    client_1 = make_client()
    amount = 3700
    response = client.post("/transactions/", json={"transaction_type": "deposit", "amount": amount, "client_id": client_1.id})
    assert response.status_code == 200

    response2 = client.get(f"/clients/{client_1.id}")
    data2 = response2.json()
    assert data2["balance"] == "4000.00"
    assert response2.status_code == 200

def test_client_deposit_incorrect(session: Session, client: TestClient, make_client):
    client_1 = make_client()
    amount = -400
    response = client.post("/transactions/", json={"transaction_type": "deposit", "amount": amount, "client_id": client_1.id})
    assert response.status_code == 400


def test_client_wrong_transaction_type(client: TestClient, session: Session, make_client):
    client_1 = make_client()
    response = client.post("/transactions/", json={"transaction_type": "AAAA", "amount": -1000, "client_id": client_1.id})
    assert response.status_code == 400


def test_get_client_not_found(client: TestClient):
    response = client.get("/clients/9999")
    assert response.status_code == 404


def test_delete_client_not_found(client: TestClient):
    response = client.delete("/clients/9999")
    assert response.status_code == 404

def test_create_client_incorrect_name(client):
    response = client.post(
        "/clients/", json={"name": "Remigiusz ccc", "balance": float(200)}
    )
    assert response.status_code == 404

def test_transfer_correct(session: Session, client: TestClient, make_client):
    client_1 = make_client(name="Adam", balance=Decimal("100.00"))
    client_2 = make_client(name="Ewa", balance=Decimal("200.00"))
    amount = 50

    response_transaction = client.post("/transfers/", json={"sender_id": client_1.id, "receiver_id": client_2.id,"amount": amount})

    response1 = client.get(f"/clients/{client_1.id}")
    data1 = response1.json()
    assert data1["balance"] == "50.00"
    response2 = client.get(f"/clients/{client_2.id}")
    data2 = response2.json()
    assert data2["balance"] == "250.00"

    assert response_transaction.status_code == 200

def test_transfer_incorrect_insufficient_funds(session: Session, client: TestClient, make_client):
    client_1 = make_client(name="Adam", balance=Decimal("100.00"))
    client_2 = make_client(name="Ewa", balance=Decimal("200.00"))
    amount = 150

    response_transaction = client.post("/transfers/", json={"sender_id": client_1.id, "receiver_id": client_2.id,  "amount": amount})

    assert response_transaction.status_code == 400

def test_transfer_incorrect_sender_not_found(session: Session, client: TestClient, make_client):
    client_1 = make_client(name="Adam", balance=Decimal("100.00"))
    # client_2 = make_client(name="Ewa", balance=Decimal("200.00"))
    amount = 150

    response_transaction = client.post("/transfers/", json={"sender_id": client_1.id, "receiver_id": 2,  "amount": amount})

    assert response_transaction.status_code == 404

def test_transfer_incorrect_zero_amount(session: Session, client: TestClient, make_client):
    sender = make_client("Adam", Decimal("300.00"))
    receiver = make_client("Ewa", Decimal("200.00"))

    resp = client.post("/transfers/", json={
        "sender_id": sender.id,
        "receiver_id": receiver.id,
        "amount": 0
    })
    assert resp.status_code == 400

    s = client.get(f"/clients/{sender.id}").json()
    r = client.get(f"/clients/{receiver.id}").json()
    assert s["balance"] == "300.00"
    assert r["balance"] == "200.00"


def test_transfer_incorrect_negative_amount(session: Session, client: TestClient, make_client):
    sender = make_client("Adam", Decimal("300.00"))
    receiver = make_client("Ewa", Decimal("200.00"))

    resp = client.post("/transfers/", json={
        "sender_id": sender.id,
        "receiver_id": receiver.id,
        "amount": -10
    })
    assert resp.status_code == 400

    s = client.get(f"/clients/{sender.id}").json()
    r = client.get(f"/clients/{receiver.id}").json()
    assert s["balance"] == "300.00"
    assert r["balance"] == "200.00"


def test_transfer_incorrect_receiver_not_found(session: Session, client: TestClient, make_client):
    sender = make_client("Adam", Decimal("100.00"))
    resp = client.post("/transfers/", json={
        "sender_id": sender.id,
        "receiver_id": 999,
        "amount": 50
    })
    assert resp.status_code == 404



def test_transfer_incorrect_same_sender_receiver(session: Session, client: TestClient, make_client):
    client_1 = make_client("Adam", Decimal("300.00"))

    resp = client.post("/transfers/", json={
        "sender_id": client_1.id,
        "receiver_id": client_1.id,
        "amount": 50
    })

    assert resp.status_code == 400
