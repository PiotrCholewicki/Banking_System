import math
from datetime import timedelta, datetime
from decimal import Decimal

from app.models.transaction import Transaction
from app.validators.value_validators import validate_amount, validate_client_name, validate_transaction_type, validate_client_id, validate_client_balance, validate_transactions


# --------------------- AMOUNT ---------------------

def test_amount_correct_data():
    assert validate_amount(Decimal(1000.5)) is True

def test_amount_negative_value():
    assert validate_amount(-5) is False

def test_amount_non_number():
    assert validate_amount("abc") is False

def test_amount_nan():
    assert validate_amount(math.nan) is False

def test_amount_inf():
    assert validate_amount(math.inf) is False

def test_amount_bool_rejected():
    assert validate_amount(True) is False

def test_amount_zero():
    assert validate_amount(0) is False


# --------------------- CLIENT NAME ---------------------

def test_client_name_correct():
    assert validate_client_name("Piotr") is True
    assert validate_client_name("Piotr Cholewicki") is True
    assert validate_client_name("Izabela Łęcka") is True
def test_client_name_incorrect():
    assert validate_client_name("iotr") is False

def test_client_name_empty_string():
    assert validate_client_name("") is False

def test_client_name_whitespace():
    assert validate_client_name("   ") is False

def test_client_name_not_string():
    assert validate_client_name(123) is False

def test_client_name_with_digits():
    assert validate_client_name("Piotr123") is False

def test_client_name_all_caps():
    assert validate_client_name("PIOTR") is False

def test_client_name_second_letter_uppercase():
    assert validate_client_name("PIotr") is False


# --------------------- TRANSACTION TYPE ---------------------

def test_correct_transaction_type():
    assert validate_transaction_type("withdrawal") is True

def test_transaction_type_incorrect_type():
    assert validate_transaction_type(True) is False

def test_transaction_type_incorrect_value():
    assert validate_transaction_type("Withdrawing") is False

def test_transaction_type_with_trailing_space():
    assert validate_transaction_type("deposit ") is False

def test_transaction_type_case_variants_rejected():
    assert validate_transaction_type("Deposit") is False
    assert validate_transaction_type("WITHDRAWAL") is False


# --------------------- CLIENT ID ---------------------

def test_client_id_correct():
    assert validate_client_id(1) is True

def test_client_id_incorrect_type():
    assert validate_client_id("d") is False

def test_client_id_incorrect_value():
    assert validate_client_id(-1) is False

def test_client_id_zero():
    assert validate_client_id(0) is False

def test_client_id_bool_rejected():
    assert validate_client_id(True) is False

def test_client_id_float_rejected():
    assert validate_client_id(1.0) is False


# ------- CLIENT BALANCE -------

def test_client_balance_correct_int():
    assert validate_client_balance(100) is True

def test_client_balance_correct_float():
    assert validate_client_balance(100.5) is True

def test_client_balance_wrong_type():
    assert validate_client_balance("100") is False

def test_client_balance_nan_inf_rejected():
    assert validate_client_balance(math.nan) is False
    assert validate_client_balance(math.inf) is False


# ------- TRANSACTIONS LIST -------

def test_transactions_list_empty_ok():
    assert validate_transactions([]) is True

def test_transactions_wrong_container_type():
    assert validate_transactions("not a list") is False



