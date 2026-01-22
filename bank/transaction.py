class Transaction:
    def __init__(self, client_name, transaction_type, amount, date):
        self.client_name = client_name
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = date

    def __str__(self):
        return f"{self.date} | {self.client_name} | {self.transaction_type} | {self.amount}"
