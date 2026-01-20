from utils.validators import validate_amount
from exceptions import InsufficientFundsError
class Client:
    def __init__(self, id, name, balance):
        self.id = id
        self.name = name
        self.balance = balance

    def withdraw(self, amount):
        #validate data
        validate_amount(amount)

        #check if user has enough funds
        if(self.balance >= amount):
            self.balance -= amount
            print(f"User {self.name} withdraws {amount}$. Now his balance is {self.balance}$.")
            return self.balance
        else:
            raise InsufficientFundsError(f"User {self.name} can't withdraw {amount}, beacuse his balance is {self.balance}")

    def deposit(self, amount):
        #validate data
        validate_amount(amount)
        self.balance += amount
        return self.balance

    #later to be done with database
    def generate_transaction_statement(self):
        print("To be done in future")





