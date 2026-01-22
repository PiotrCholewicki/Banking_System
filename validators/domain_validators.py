from validators.value_validators import *

from bank.client import Client
from bank.transaction import Transaction

#validating whole objets
def validate_whole_transaction(transaction):

    if not isinstance(transaction, Transaction):
        raise TypeError("transaction must be a Transaction instance")

    validate_client_name(transaction.client_name)
    validate_transaction_type(transaction.transaction_type)
    validate_amount(transaction.amount)
    validate_date(transaction.date)
    return True

def validate_client(client):

    if not isinstance(client, Client):
        raise TypeError("client must be a Client instance")

    validate_client_id(client.id)
    validate_client_name(client.name)
    validate_client_balance(client.balance)
    validate_transactions(client.transactions)
    return True