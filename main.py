from bank.bank import Bank
from bank.client import Client

def main():
    client_1 = Client(1, "Piotr", 2000)
    client_2 = Client(2, "Dominika", 1000)
    bank = Bank()
    bank.add_client(client_1)
    bank.add_client(client_2)
    bank.deposit(client_1.id, 200)
    bank.withdraw(client_1.id, 300)
    bank.withdraw(client_2.id, 700)
    bank.withdraw(client_2.id, 300)
    client_1.print_statement()
    client_2.print_statement()
    bank.get_all_balances()



if __name__ == '__main__':
    main()


