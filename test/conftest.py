from datetime import timedelta
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.auth.auth import get_password_hash, create_access_token
from app.main import app
from app.database import get_session
from app.models.client import Client
from app.models.user import User


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def create_user(session):
    def _create(
        username="test",
        password="1234",
        role="client",
        is_active=True,
        client_balance=100,
    ):
        user = User(
            username=username,
            hashed_password=get_password_hash(password),
            role=role,
            is_active=is_active,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        client = Client(name=username, balance=Decimal(client_balance))
        session.add(client)
        session.commit()
        session.refresh(client)

        user.client_id = client.id
        session.commit()
        return user

    return _create


@pytest.fixture
def make_token():
    def _token(user: User):
        return create_access_token(
            data={"sub": user.username},
            role=user.role,
            expires_delta=timedelta(minutes=30),
        )

    return _token


@pytest.fixture
def auth_client(client: TestClient, make_token):
    def _auth_client(user: User):
        token = make_token(user)
        client.headers = {"Authorization": f"Bearer {token}"}
        return client

    return _auth_client
