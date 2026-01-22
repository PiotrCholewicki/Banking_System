class Client:
    def __init__(self, id, name, balance):
        self.id = id
        self.name = name
        self.balance = balance
        self.transactions = []

    def __str__(self):
        return f"{self.id}, {self.name}, {self.balance}, {self.transactions}"

    def print_statement(self):
        print(f"Transaction history for {self.name}")
        for t in self.transactions:
            print(t)









