def validate_amount(amount):
    if not isinstance(amount, (int,float)):
        raise TypeError("Amount must be a number")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    return True