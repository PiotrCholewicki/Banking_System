
import pytest
from validators.bank_validators import *
from bank.bank import Bank
from bank.client import Client
from bank.transaction import Transaction


# -------------------------- FIXTURES --------------------------

@pytest.fixture
def client():
    return Client(1, "Piotr", 1000)

@pytest.fixture
def another_client():
    return Client(2, "Dominika", 500)

@pytest.fixture
def transaction():
    return Transaction("Piotr", "withdrawal", 200, datetime.now())

@pytest.fixture
def bank_correct(client, transaction):
    return Bank([transaction], [client])

@pytest.fixture
def bank_empty():
    return Bank([], [])

@pytest.fixture
def bank_incorrect():
    return -1

@pytest.fixture
def bank_incorrect_client_list():
    return Bank([], "not-a-list")

@pytest.fixture
def bank_incorrect_client_instances():
    return Bank([], [1, 2, "wrong"])

@pytest.fixture
def bank_incorrect_transaction_list():
    return Bank("not-a-list", [])

@pytest.fixture
def bank_incorrect_transaction_instances():
    return Bank([1, 2, "wrong"], [])


# -------------------------- validate_bank_instance --------------------------

def test_validate_bank_instance(bank_correct):
    assert validate_bank_instance(bank_correct) is True

def test_validate_bank_instance_invalid(bank_incorrect):
    with pytest.raises(TypeError):
        validate_bank_instance(bank_incorrect)


# -------------------------- validate_bank_clients --------------------------

def test_validate_bank_clients_correct(bank_correct):
    assert validate_bank_clients(bank_correct) is True

def test_validate_bank_clients_not_list(bank_incorrect_client_list):
    with pytest.raises(TypeError):
        validate_bank_clients(bank_incorrect_client_list)

def test_validate_bank_clients_invalid_instances(bank_incorrect_client_instances):
    with pytest.raises(TypeError):
        validate_bank_clients(bank_incorrect_client_instances)


# -------------------------- validate_bank_transactions --------------------------

def test_validate_bank_transactions_correct(bank_correct):
    assert validate_bank_transactions(bank_correct) is True

def test_validate_bank_transactions_not_list(bank_incorrect_transaction_list):
    with pytest.raises(TypeError):
        validate_bank_transactions(bank_incorrect_transaction_list)

def test_validate_bank_transactions_invalid_instances(bank_incorrect_transaction_instances):
    with pytest.raises(TypeError):
        validate_bank_transactions(bank_incorrect_transaction_instances)


# -------------------------- validate_client_id_in_bank --------------------------

def test_validate_client_id_in_bank_correct(bank_correct):
    assert validate_client_id_in_bank(bank_correct, 1) is True

def test_validate_client_id_in_bank_wrong_id(bank_correct):
    with pytest.raises(ValueError):
        validate_client_id_in_bank(bank_correct, 999)

def test_validate_client_id_in_bank_wrong_type(bank_correct):
    with pytest.raises(TypeError):
        validate_client_id_in_bank(bank_correct, "wrong")


# -------------------------- validate_client_object_in_bank --------------------------

def test_validate_client_object_in_bank_correct(bank_correct, client):
    assert validate_client_object_in_bank(bank_correct, client) is True

def test_validate_client_object_in_bank_not_a_client(bank_correct):
    with pytest.raises(TypeError):
        validate_client_object_in_bank(bank_correct, "not-a-client")

def test_validate_client_object_in_bank_wrong_client(bank_correct, another_client):
    with pytest.raises(ValueError):
        validate_client_object_in_bank(bank_correct, another_client)


# -------------------------- validate_bank_can_withdraw --------------------------

def test_validate_bank_can_withdraw_correct(client):
    assert validate_bank_can_withdraw(client, 500) is True

def test_validate_bank_can_withdraw_insufficient(client):
    with pytest.raises(ValueError):
        validate_bank_can_withdraw(client, 999999)


# -------------------------- validate_bank_deposit_params --------------------------

def test_validate_bank_deposit_params_correct(client):
    assert validate_bank_deposit_params(client, 100) is True

def test_validate_bank_deposit_params_wrong_amount(client):
    with pytest.raises(TypeError):
        validate_bank_deposit_params(client, "wrong")


# -------------------------- validate_bank_withdraw_params --------------------------

def test_validate_bank_withdraw_params_correct(client):
    assert validate_bank_withdraw_params(client, 100) is True

def test_validate_bank_withdraw_params_insufficient_funds(client):
    with pytest.raises(ValueError):
        validate_bank_withdraw_params(client, 999999)

def test_validate_bank_withdraw_params_wrong_amount(client):
    with pytest.raises(TypeError):
        validate_bank_withdraw_params(client, "wrong")


# -------------------------- validate_bank_integrity --------------------------

def test_validate_bank_integrity_correct(bank_correct):
    assert validate_bank_integrity(bank_correct) is True

def test_validate_bank_integrity_incorrect_instance(bank_incorrect):
    with pytest.raises(TypeError):
        validate_bank_integrity(bank_incorrect)

def test_validate_bank_integrity_incorrect_clients(bank_incorrect_client_instances):
    with pytest.raises(TypeError):
        validate_bank_integrity(bank_incorrect_client_instances)

def test_validate_bank_integrity_incorrect_transactions(bank_incorrect_transaction_instances):
    with pytest.raises(TypeError):
        validate_bank_integrity(bank_incorrect_transaction_instances)
