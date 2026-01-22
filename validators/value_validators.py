from datetime import datetime
import re
import math

from bank.transaction import Transaction


#validating simple fields
def validate_amount(amount):
    return is_positive_int_or_float(amount)


def validate_client_name(client_name):
    if not isinstance(client_name, str):
        raise TypeError("Client name must be a string.")

    pattern = r'^[A-Z][a-z]+$'
    if not re.match(pattern, client_name):
        raise ValueError("Client name must start with a capital letter and contain only lowercase letters afterwards.")
    return True


def validate_transaction_type(transaction_type):
    allowed_transaction_types = {"deposit", "withdrawal"}

    if not isinstance(transaction_type, str):
        raise TypeError("Transaction type must be a string.")

    if not (transaction_type in allowed_transaction_types):
        raise ValueError("Illegal transaction type")
    return True


def validate_date(date):
    if not isinstance(date, datetime):
        raise TypeError("Date must be a datetime object")

    if date > datetime.now():
        raise ValueError("Date cannot be in the future")

    return True

def validate_client_id(client_id):
    if isinstance(client_id, bool):
        raise TypeError("Client_id cannot be boolean")
    if not isinstance(client_id, int):
        raise TypeError("Client_id must be an integer or float")
    if math.isnan(client_id) or math.isinf(client_id):
        raise ValueError("Client_id cannot be NaN or infinite")
    if client_id <= 0:
        raise ValueError("Client id cannot be <= 0")
    return True

def validate_client_balance(balance):
    return is_positive_int_or_float(balance)

def validate_transactions(transactions):
    if not isinstance(transactions, list):
        raise TypeError("Transactions must be a list")

    for t in transactions:
        if not isinstance(t, Transaction):
            raise TypeError("Each element must be a Transaction object")

    return True

def is_positive_int_or_float(param):
    if isinstance(param, bool):
        raise TypeError("Number cannot be boolean")
    if not isinstance(param, (int, float)):
        raise TypeError("Number must be an integer or float")
    if math.isnan(param) or math.isinf(param):
        raise ValueError("Number cannot be NaN or infinite")
    if param <= 0:
        raise ValueError("Number cannot be <= 0")
    return True