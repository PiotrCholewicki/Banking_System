import math
import pytest
from datetime import datetime, timedelta

from validators.domain_validators import (
    validate_whole_transaction,
    validate_client
)

from bank.client import Client
from bank.transaction import Transaction


# VALIDATE WHOLE TRANSACTION
def test_validate_whole_transaction_correct():
    t = Transaction("Piotr", "withdrawal", 100, datetime.now())
    assert validate_whole_transaction(t) is True


def test_validate_whole_transaction_wrong_type():
    with pytest.raises(TypeError):
        validate_whole_transaction("not a transaction")


def test_validate_whole_transaction_invalid_client_name():
    t = Transaction("piotr", "withdrawal", 100, datetime.now())
    with pytest.raises(ValueError):
        validate_whole_transaction(t)


def test_validate_whole_transaction_invalid_transaction_type():
    t = Transaction("Piotr", "invalid", 100, datetime.now())
    with pytest.raises(ValueError):
        validate_whole_transaction(t)


def test_validate_whole_transaction_invalid_amount():
    t = Transaction("Piotr", "withdrawal", -100, datetime.now())
    with pytest.raises(ValueError):
        validate_whole_transaction(t)


def test_validate_whole_transaction_invalid_date_type():
    t = Transaction("Piotr", "withdrawal", 100, "today")
    with pytest.raises(TypeError):
        validate_whole_transaction(t)


def test_validate_whole_transaction_future_date():
    t = Transaction("Piotr", "withdrawal", 100, datetime.now() + timedelta(days=1))
    with pytest.raises(ValueError):
        validate_whole_transaction(t)



# VALIDATE CLIENT

def test_validate_client_correct():
    client = Client(1, "Piotr", 1000)
    assert validate_client(client) is True


def test_validate_client_wrong_type():
    with pytest.raises(TypeError):
        validate_client("not a client")


def test_validate_client_invalid_id_type():
    client = Client("id", "Piotr", 1000)
    with pytest.raises(TypeError):
        validate_client(client)


def test_validate_client_invalid_id_value():
    client = Client(0, "Piotr", 1000)
    with pytest.raises(ValueError):
        validate_client(client)


def test_validate_client_invalid_name():
    client = Client(1, "piotr", 1000)
    with pytest.raises(ValueError):
        validate_client(client)


def test_validate_client_invalid_balance_type():
    client = Client(1, "Piotr", "wrong")
    with pytest.raises(TypeError):
        validate_client(client)


def test_validate_client_invalid_balance_nan():
    client_nan = Client(1, "Piotr", math.nan)
    with pytest.raises(ValueError):
        validate_client(client_nan)

def test_validate_client_invalid_balance_inf():
    client_inf = Client(1, "Piotr", math.inf)
    with pytest.raises(ValueError):
        validate_client(client_inf)

def test_validate_client_invalid_transactions_wrong_type():
    client = Client(1, "Piotr", 1000)
    client.transactions = "not a list"
    with pytest.raises(TypeError):
        validate_client(client)

def test_validate_client_invalid_transactions_wrong_element_type():
    client = Client(1, "Piotr", 1000)
    client.transactions = ["not a transaction"]
    with pytest.raises(TypeError):
        validate_client(client)
