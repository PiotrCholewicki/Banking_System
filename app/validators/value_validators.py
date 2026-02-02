from datetime import datetime
import re
import math

from decimal import Decimal

from app.models.transaction import Transaction


# validating simple fields
def validate_amount(amount):
    if not isinstance(amount, Decimal):
        return False
    if amount <= 0:
        return False
    return True


def validate_client_name(client_name):
    if not isinstance(client_name, str):
        return False

    NAME_REGEX = r"^[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?: [A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)?$"
    if not re.match(NAME_REGEX, client_name):
        return False
    return True


def validate_transaction_type(transaction_type):
    allowed_transaction_types = {"deposit", "withdrawal"}

    if not isinstance(transaction_type, str):
        return False

    if not (transaction_type in allowed_transaction_types):
        return False
    return True


def validate_client_id(client_id):
    if isinstance(client_id, bool):
        return False
    if not isinstance(client_id, int):
        return False
    if math.isnan(client_id) or math.isinf(client_id):
        return False
    if client_id <= 0:
        return False
    return True


def validate_client_balance(balance):
    return is_positive_int_or_float(balance)


def validate_transactions(transactions):
    if not isinstance(transactions, list):
        return False

    for t in transactions:
        if not isinstance(t, Transaction):
            return False

    return True


def is_positive_int_or_float(param):
    if isinstance(param, bool):
        return False
    if not isinstance(param, (int, float)):
        return False
    if math.isnan(param) or math.isinf(param):
        return False
    if param <= 0:
        return False
    return True
