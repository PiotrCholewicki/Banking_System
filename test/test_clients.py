from sqlmodel import select

from app.models.client import Client
from app.models.transaction import Transaction
from app.routes.clients import delete_client


def test_get_my_client(auth_client, create_user):
    user = create_user(client_balance=250)
    c = auth_client(user)

    response = c.get("/clients/me/")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "test"
    assert data["balance"] == "250.00"


def test_get_my_transactions_correct(auth_client, create_user, session):
    user = create_user(username="Piotr", client_balance=300)
    c = auth_client(user)

    tx = c.post("/transactions/", json={"transaction_type": "deposit", "amount": 200})
    assert tx.status_code == 200

    response = c.get("/clients/me/transactions")
    assert response.status_code == 200

    data = response.json()["items"]
    transaction = data[0]

    assert transaction["transaction_type"] == "deposit"
    assert transaction["amount"] == "200.00"


def test_my_transactions_multiple(auth_client, create_user):
    user = create_user(client_balance=1000)
    c = auth_client(user)

    c.post("/transactions/", json={"transaction_type": "deposit", "amount": 200})
    c.post("/transactions/", json={"transaction_type": "withdrawal", "amount": 50})

    r = c.get("/clients/me/transactions")
    data = r.json()["items"]

    assert data[0]["transaction_type"] == "deposit"
    assert data[1]["transaction_type"] == "withdrawal"
    assert c.get("/clients/me").json()["balance"] == "1150.00"


def test_get_my_client_unauthorized(client):
    response = client.get("/clients/me/")
    assert response.status_code == 401


def test_get_my_client_invalid_token(client):
    client.headers = {"Authorization": "Bearer invalid.token"}

    resp = client.get("/clients/me/")
    assert resp.status_code == 401


def test_get_my_client_not_found(auth_client, create_user, session):
    user = create_user()
    client_obj = session.get(Client, user.client_id)
    session.delete(client_obj)
    session.commit()

    c = auth_client(user)
    resp = c.get("/clients/me/")
    assert resp.status_code == 404


def test_my_transactions_unauthorized(client):
    resp = client.get("/clients/me/transactions")
    assert resp.status_code == 401


def test_my_transactions_client_missing(auth_client, create_user, session):
    user = create_user()
    client_obj = session.get(Client, user.client_id)
    session.delete(client_obj)
    session.commit()

    c = auth_client(user)
    resp = c.get("/clients/me/transactions")
    assert resp.status_code == 404


def test_my_transactions_empty(auth_client, create_user):
    user = create_user(client_balance=500)
    c = auth_client(user)

    resp = c.get("/clients/me/transactions")
    assert resp.status_code == 200
    assert resp.json()["items"] == []


def test_delete_client_deletes_transactions(session, create_user):
    user = create_user(client_balance=500)

    # new transaction
    tx = Transaction(
        amount=100,
        transaction_type="deposit",
        client_id=user.client_id,
    )
    session.add(tx)
    session.commit()

    # transaction in db
    assert (
        session.exec(
            select(Transaction).where(Transaction.client_id == user.client_id)
        ).first()
        is not None
    )

    delete_client(user.client_id, session)

    # client deleted
    assert session.get(Client, user.client_id) is None

    # transactions deleted
    assert (
        session.exec(
            select(Transaction).where(Transaction.client_id == user.client_id)
        ).first()
        is None
    )


def test_register_creates_client_correctly(client, session):
    payload = {"username": "janek", "password": "abcd1234", "balance": 250}

    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 201

    created_client = session.exec(select(Client).where(Client.name == "janek")).first()

    assert created_client is not None
    assert str(created_client.balance) == "250.00"
