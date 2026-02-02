from app.models.client import Client


def test_transfer_correct(auth_client, create_user, session):
    sender = create_user(username="Adam", client_balance=300)
    receiver = create_user(username="Ewa", client_balance=200)

    c = auth_client(sender)

    resp = c.post(
        "/transfers/", json={"receiver_id": receiver.client_id, "amount": 100}
    )

    assert resp.status_code == 200

    s = session.get(Client, sender.client_id)
    r = session.get(Client, receiver.client_id)

    assert str(s.balance) == "200.00"
    assert str(r.balance) == "300.00"


def test_transfer_insufficient_funds(auth_client, create_user):
    sender = create_user(username="Adam", client_balance=50)
    receiver = create_user(username="Ewa", client_balance=200)

    c = auth_client(sender)

    resp = c.post(
        "/transfers/", json={"receiver_id": receiver.client_id, "amount": 100}
    )

    assert resp.status_code == 400


def test_transfer_receiver_not_found(auth_client, create_user):
    sender = create_user(username="Adam", client_balance=300)
    c = auth_client(sender)

    resp = c.post("/transfers/", json={"receiver_id": 9999, "amount": 50})


def test_transfer_sender_missing(auth_client, create_user, session):
    sender = create_user(username="Adam", client_balance=300)
    receiver = create_user(username="Ewa", client_balance=200)

    # usuwamy klienta nadawcy
    session.delete(session.get(Client, sender.client_id))
    session.commit()

    c = auth_client(sender)

    resp = c.post("/transfers/", json={"receiver_id": receiver.client_id, "amount": 50})

    assert resp.status_code == 404


def test_transfer_zero_amount(auth_client, create_user):
    sender = create_user(username="Adam", client_balance=300)
    receiver = create_user(username="Ewa", client_balance=200)

    c = auth_client(sender)

    resp = c.post("/transfers/", json={"receiver_id": receiver.client_id, "amount": 0})

    assert resp.status_code == 400


def test_transfer_negative_amount(auth_client, create_user):
    sender = create_user(username="Adam", client_balance=300)
    receiver = create_user(username="Ewa", client_balance=200)

    c = auth_client(sender)

    resp = c.post(
        "/transfers/", json={"receiver_id": receiver.client_id, "amount": -10}
    )

    assert resp.status_code == 400


def test_transfer_same_sender_receiver(auth_client, create_user):
    user = create_user(client_balance=300)
    c = auth_client(user)

    resp = c.post("/transfers/", json={"receiver_id": user.client_id, "amount": 50})

    assert resp.status_code == 400


def test_transfer_unauthorized(client, create_user):
    receiver = create_user(client_balance=200)

    resp = client.post(
        "/transfers/", json={"receiver_id": receiver.client_id, "amount": 50}
    )

    assert resp.status_code == 401


def test_transfer_inactive_user(make_token, client, create_user):
    user = create_user(client_balance=300, is_active=False)
    token = make_token(user)

    client.headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        "/transfers/", json={"receiver_id": user.client_id, "amount": 50}
    )

    assert resp.status_code == 400
