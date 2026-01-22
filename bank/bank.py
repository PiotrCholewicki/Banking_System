from bank.transaction import Transaction
from datetime import datetime
from exceptions import InsufficientFundsError
class Bank:

    def __init__(self, transactions=None, clients=None):
        self.transactions = transactions if transactions is not None else []
        self.clients = clients if clients is not None else []

    def add_client(self, client_id):
        self.clients.append(client_id)

    def delete_client(self, client_id):
        self.clients.remove(client_id)

    def get_client_by_id(self, searched_id):
        for client in self.clients:
            if client.id == searched_id:
                return client
        return -1

    def get_all_balances(self):
        for client in self.clients:
            print(f"{client.id}, {client.balance}")


    def register_transaction(self, client, transaction):
        self.transactions.append(transaction)
        client.transactions.append(transaction)

    def withdraw(self, client_id, amount):
        client = self.get_client_by_id(client_id)
        from validators.value_validators import validate_amount
        from validators.domain_validators import validate_client, validate_whole_transaction
        validate_client(client)
        validate_amount(amount)
        if client.balance < amount:
            raise InsufficientFundsError(f"Client {client.name} can't withdraw {amount}, beacuse his balance is {client.balance}")

        transaction = Transaction(client.name, "withdrawal", amount, datetime.now())
        validate_whole_transaction(transaction)
        self.register_transaction(client, transaction)
        client.balance -= amount
        print(f"User {client.name} withdraws {amount}$. Now his balance is {client.balance}$.")


    def deposit(self, client_id, amount):
        client = self.get_client_by_id(client_id)
        from validators.value_validators import validate_amount
        from validators.domain_validators import validate_client, validate_whole_transaction
        validate_client(client)
        validate_amount(amount)
        transaction = Transaction(client.name, "deposit", amount, datetime.now())
        validate_whole_transaction(transaction)
        self.register_transaction(client, transaction)
        client.balance += amount
        print(f"User {client.name} deposits {amount}$. Now his balance is {client.balance}$.")


    def get_all_transactions(self):
        for t in self.transactions:
            print(t)

