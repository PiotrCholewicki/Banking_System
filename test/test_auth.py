import pytest

from app.auth.auth import (
    get_password_hash,
    verify_password,
    authenticate_user,
    get_current_user,
    require_admin,
    ensure_client_access,
)
from app.models.client import Client
from test.conftest import make_token

import pytest
from fastapi import HTTPException
from app.auth.auth import get_current_active_user


def test_register_user_correct(client, session):
    payload = {"username": "Piotr", "password": "test1234", "balance": 150}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data


def test_register_user_incorrect_user_already_exists(client, session):
    payload = {"username": "Piotr", "password": "test1234", "balance": 150}
    client.post("/auth/register", json=payload)

    payload = {"username": "Piotr", "password": "test1234", "balance": 150}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409


def test_register_password_too_short(client, session):
    payload = {"username": "Piotr", "password": "aa", "balance": 150}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_login_correct(client, create_user):
    user = create_user(username="test", password="1234")
    response = client.post(
        "/auth/login/",
        data={"username": "test", "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_correct_incorrect_password(client, create_user):
    user = create_user(username="test", password="1234")
    response = client.post(
        "/auth/login/",
        data={"username": "test", "password": "1234555"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


def test_delete_me(auth_client, create_user):
    user = create_user(username="test", password="1234")
    c = auth_client(user)
    response = c.delete("/auth/delete")
    assert response.status_code == 204


def test_password_hash_and_verify():
    plain = "secret123"
    hashed = get_password_hash(plain)

    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("wrongpass", hashed) is False


def test_authenticate_user_correct(create_user, session):
    user = create_user(username="piotr", password="abcd")
    authenticated = authenticate_user(session, "piotr", "abcd")
    assert authenticated is not None
    assert authenticated.id == user.id


def test_authenticate_user_invalid(create_user, session):
    create_user(username="piotr", password="abcd")

    assert authenticate_user(session, "baduser", "abcd") is None
    assert authenticate_user(session, "piotr", "wrong") is None


@pytest.mark.asyncio
async def test_get_current_user_correct(create_user, make_token, session):
    user = create_user(username="piotr", password="1234")

    token = make_token(user)

    resolved = await get_current_user(token=token, session=session)

    assert resolved.id == user.id


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(session):
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token="bad.token.value", session=session)

    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_active_user_inactive(create_user):
    user = create_user(is_active=False)

    with pytest.raises(HTTPException) as exc:
        await get_current_active_user(user)

    assert exc.value.status_code == 400


def test_require_admin_ok(create_user):
    admin = create_user(role="admin")
    assert require_admin(admin) is None


def test_require_admin_forbidden(create_user):
    user = create_user(role="client")
    with pytest.raises(HTTPException) as exc:
        require_admin(user)
    assert exc.value.status_code == 403


def test_ensure_client_access_ok_for_self(create_user, session):
    user = create_user()
    client = session.get(Client, user.client_id)

    assert ensure_client_access(client, user) is None


def test_ensure_client_access_ok_for_admin(create_user, session):
    admin = create_user(role="admin")
    client_user = create_user(username="piotr")
    client = session.get(Client, client_user.client_id)

    assert ensure_client_access(client, admin) is None


def test_ensure_client_access_forbidden(create_user, session):
    user1 = create_user(username="a", client_balance=100)
    user2 = create_user(username="b", client_balance=200)

    client2 = session.get(Client, user2.client_id)

    with pytest.raises(HTTPException) as exc:
        ensure_client_access(client2, user1)

    assert exc.value.status_code == 403


def test_delete_admin_forbidden(auth_client, create_user):
    admin = create_user(username="admin", role="admin")
    c = auth_client(admin)

    resp = c.delete("/auth/delete/")
    assert resp.status_code == 400


def test_register_invalid_password(client):
    payload = {"username": "piotr", "password": "abc", "balance": 100}

    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 400
