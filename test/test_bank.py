import pytest
from exceptions import InsufficientFundsError
from bank.bank import Bank
from bank.client import Client
from bank.transaction import Transaction
from datetime import datetime


# ---------------- FIXTURES ----------------

@pytest.fixture
def client():
    return Client(1, "Piotr", 1000)

@pytest.fixture
def transaction():
    return Transaction("Piotr", "withdrawal", 200, datetime.now())

@pytest.fixture
def bank(client, transaction):
    return Bank([transaction], [client])

# ---------------- WITHDRAW ----------------

def test_withdraw_correct(bank, client):
    bank.withdraw(client.id, 300)
    assert client.balance == 700


def test_withdraw_negative_amount(bank, client):
    with pytest.raises(ValueError):
        bank.withdraw(client.id, -300)


def test_withdraw_incorrect_type(bank, client):
    with pytest.raises(TypeError):
        bank.withdraw(client.id, "aa")


def test_withdraw_insufficient_funds(bank, client):
    with pytest.raises(InsufficientFundsError):
        bank.withdraw(client.id, 2000)


def test_withdraw_incorrect_client_type(bank):
    with pytest.raises(TypeError):
        bank.withdraw(100, 100)   # invalid client object


# ---------------- DEPOSIT ----------------

def test_deposit_correct(bank, client):
    bank.deposit(client.id, 300)
    assert client.balance == 1300


def test_deposit_incorrect_type(bank, client):
    with pytest.raises(TypeError):
        bank.deposit(client.id, "a")


def test_deposit_non_positive_value(bank, client):
    with pytest.raises(ValueError):
        bank.deposit(client.id, -1)


def test_deposit_incorrect_client_type(bank):
    with pytest.raises(TypeError):
        bank.deposit("aaa", 100)
