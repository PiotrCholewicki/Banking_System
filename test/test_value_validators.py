from datetime import timedelta, timezone

from validators.value_validators import *
import pytest
# --------------------- AMOUNT ---------------------

def test_amount_correct_data():
    assert validate_amount(1000.5) is True

def test_amount_negative_value():
    with pytest.raises(ValueError):
        validate_amount(-5)

def test_amount_non_number():
    with pytest.raises(TypeError):
        validate_amount("abc")

def test_amount_nan():
    with pytest.raises(ValueError):
        validate_amount(math.nan)

def test_amount_inf():
    with pytest.raises(ValueError):
        validate_amount(math.inf)

def test_amount_bool_rejected():

    with pytest.raises(TypeError):
        validate_amount(True)

def test_amount_zero():
    with pytest.raises(ValueError):
        validate_amount(0)


# --------------------- CLIENT NAME ---------------------

def test_client_name_correct():
    assert validate_client_name("Piotr") is True

def test_client_name_incorrect():
    with pytest.raises(ValueError):
        validate_client_name("iotr")

def test_client_name_empty_string():
    with pytest.raises(ValueError):
        validate_client_name("")

def test_client_name_whitespace():
    with pytest.raises(ValueError):
        validate_client_name("   ")

def test_client_name_not_string():
    with pytest.raises(TypeError):
        validate_client_name(123)

def test_client_name_with_digits():
    with pytest.raises(ValueError):
        validate_client_name("Piotr1")

def test_client_name_all_caps():
    with pytest.raises(ValueError):
        validate_client_name("PIOTR")


# --------------------- DATE ---------------------

def test_date_correct():
    assert validate_date(datetime.now()) is True

def test_date_incorrect_type():
    with pytest.raises(TypeError):
        validate_date(123)

def test_date_from_future():
    with pytest.raises(ValueError):
        validate_date(datetime.now() + timedelta(days=1))


def test_date_none():
    with pytest.raises(TypeError):
        validate_date(None)

# --------------------- TRANSACTION TYPE ---------------------

def test_correct_transaction_type():
    assert validate_transaction_type("withdrawal") is True

def test_transaction_type_incorrect_type():
    with pytest.raises(TypeError):
        validate_transaction_type(True)

def test_transaction_type_incorrect_value():
    with pytest.raises(ValueError):
        validate_transaction_type("Withdrawing")

def test_transaction_type_with_trailing_space():
    with pytest.raises(ValueError):
        validate_transaction_type("deposit ")

def test_transaction_type_case_variants_rejected():
    with pytest.raises(ValueError):
        validate_transaction_type("Deposit")
    with pytest.raises(ValueError):
        validate_transaction_type("WITHDRAWAL")


# --------------------- CLIENT ID ---------------------

def test_client_id_correct():
    assert validate_client_id(1) is True

def test_client_id_incorrect_type():
    with pytest.raises(TypeError):
        validate_client_id("d")

def test_client_id_incorrect_value():
    with pytest.raises(ValueError):
        validate_client_id(-1)


def test_client_id_zero():
    with pytest.raises(ValueError):
        validate_client_id(0)

def test_client_id_bool_rejected():
    with pytest.raises(TypeError):
        validate_client_id(True)

def test_client_id_float_rejected():
    with pytest.raises(TypeError):
        validate_client_id(1.0)


# ------- CLIENT BALANCE -------

def test_client_balance_correct_int():
    assert validate_client_balance(100) is True

def test_client_balance_correct_float():
    assert validate_client_balance(100.5) is True

def test_client_balance_wrong_type():
    with pytest.raises(TypeError):
        validate_client_balance("100")

def test_client_balance_nan_inf_rejected():

    with pytest.raises(ValueError):
        validate_client_balance(math.nan)
    with pytest.raises(ValueError):
        validate_client_balance(math.inf)


# ------- TRANSACTIONS LIST -------

def test_transactions_list_empty_ok():
    assert validate_transactions([]) is True

def test_transactions_wrong_container_type():
    with pytest.raises(TypeError):
        validate_transactions("not a list")

def test_transactions_wrong_element_type():
    with pytest.raises(TypeError):
        validate_transactions([Transaction("Piotr", "deposit", 10, datetime.now()), "x"])



