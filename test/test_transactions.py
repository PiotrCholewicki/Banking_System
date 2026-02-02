def test_deposit_correct(auth_client, create_user, session):
    user = create_user(username="Piotr", client_balance=300)
    c = auth_client(user)

    response = c.post(
        "/transactions/", json={"transaction_type": "deposit", "amount": 200}
    )

    assert response.status_code == 200

    updated = c.get("/clients/me/").json()
    assert updated["balance"] == "500.00"


def test_deposit_incorrect_negative_amount(auth_client, create_user, session):
    user = create_user(username="Piotr", client_balance=300)
    c = auth_client(user)

    response = c.post(
        "/transactions/", json={"transaction_type": "deposit", "amount": -200}
    )

    assert response.status_code == 400


def test_withdrawal_correct(auth_client, create_user):
    user = create_user(client_balance=100)
    c = auth_client(user)

    resp = c.post(
        "/transactions/", json={"transaction_type": "withdrawal", "amount": 50}
    )

    assert resp.status_code == 200
    updated = c.get("/clients/me/").json()
    assert updated["balance"] == "50.00"


def test_withdrawal_insufficient_funds(auth_client, create_user):
    user = create_user(client_balance=100)
    c = auth_client(user)

    resp = c.post(
        "/transactions/", json={"transaction_type": "withdrawal", "amount": 200}
    )

    assert resp.status_code == 400


def test_transactions_client_does_not_exist(client, create_user):
    resp = client.post(
        "/transactions/", json={"transaction_type": "withdrawal", "amount": 200}
    )

    assert resp.status_code == 401
