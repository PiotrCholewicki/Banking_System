from decimal import Decimal

import pytest
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models.client import Client


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

def test_delete_client(session: Session, client: TestClient):
    client_1 = Client(name="Adam", balance=Decimal("300.00"))
    session.add(client_1)
    session.commit()
    response = client.delete(f"/clients/{client_1.id}")
    client_in_db = session.get(Client, client_1.id)
    assert response.status_code == 204
    assert client_in_db is None

def test_client_withdrawal_correct(session: Session, client: TestClient):
    client_1 = Client(name="Adam", balance=Decimal("300.00"))
    session.add(client_1)
    session.commit()
    amount = 200
    response = client.put(f"/clients/{client_1.id}/{amount}/withdrawal")
    data = response.json()
    assert data["balance"] == "100.00"
    assert response.status_code == 200

def test_client_withdrawal_incorrect(session: Session, client: TestClient):
    client_1 = Client(name="Adam", balance=Decimal("300.00"))
    session.add(client_1)
    session.commit()
    amount = 400
    response = client.put(f"/clients/{client_1.id}/{amount}/withdrawal")
    assert response.status_code == 400

def test_client_deposit_correct(session: Session, client: TestClient):
    client_1 = Client(name="Adam", balance=Decimal("300.00"))
    session.add(client_1)
    session.commit()
    amount = 3700
    response = client.put(f"/clients/{client_1.id}/{amount}/deposit")
    data = response.json()
    assert data["balance"] == "4000.00"
    assert response.status_code == 200

def test_client_deposit_incorrect(session: Session, client: TestClient):
    client_1 = Client(name="Adam", balance=Decimal("300.00"))
    session.add(client_1)
    session.commit()
    amount = -400
    response = client.put(f"/clients/{client_1.id}/{amount}/deposit")
    assert response.status_code == 400


def test_client_wrong_transaction_type(client: TestClient, session: Session):
    client_1 = Client(name="Adam", balance=Decimal("100.00"))
    session.add(client_1)
    session.commit()
    response = client.put(f"/clients/{client_1.id}/50/unknown_type")
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

