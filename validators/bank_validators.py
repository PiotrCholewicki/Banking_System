from validators.domain_validators import *
from bank.bank import Bank
from bank.client import Client
from bank.transaction import Transaction



# ------------------------ BASIC STRUCTURE ------------------------

def validate_bank_instance(bank):
    if not isinstance(bank, Bank):
        raise TypeError("bank must be a Bank instance")
    return True


def validate_bank_clients(bank):
    if not isinstance(bank.clients, list):
        raise TypeError("bank.clients must be a list")

    for c in bank.clients:
        if not isinstance(c, Client):
            raise TypeError("bank.clients must contain Client objects")

    return True


def validate_bank_transactions(bank):
    if not isinstance(bank.transactions, list):
        raise TypeError("bank.transactions must be a list")

    for t in bank.transactions:
        if not isinstance(t, Transaction):
            raise TypeError("bank.transactions must contain Transaction objects")

    return True


# ------------------------ CLIENT EXISTENCE ------------------------

def validate_client_id_in_bank(bank, client_id):
    validate_bank_instance(bank)
    validate_client_id(client_id)

    for client in bank.clients:
        if client.id == client_id:
            return True

    raise ValueError(f"Client with id {client_id} not found in bank")


def validate_client_object_in_bank(bank, client):
    validate_bank_instance(bank)

    if not isinstance(client, Client):
        raise TypeError("Argument client must be a Client instance")

    if client not in bank.clients:
        raise ValueError("Client does not belong to this bank")

    return True


# ------------------------ TRANSACTION-RELATED ------------------------

def validate_bank_can_withdraw(client, amount):
    if client.balance < amount:
        raise ValueError(f"Client {client.name} does not have enough balance")
    return True


def validate_bank_deposit_params(client, amount):
    validate_client(client)
    validate_amount(amount)
    return True


def validate_bank_withdraw_params(client, amount):
    validate_client(client)
    validate_amount(amount)
    validate_bank_can_withdraw(client, amount)
    return True


# ------------------------ BANK INTEGRITY ------------------------

def validate_bank_integrity(bank):
    validate_bank_instance(bank)
    validate_bank_clients(bank)
    validate_bank_transactions(bank)
    return True
