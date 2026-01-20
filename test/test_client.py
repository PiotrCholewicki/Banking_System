import unittest
from client import Client
from exceptions import InsufficientFundsError


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(1, "Piotr", 1000)

    def test_withdraw_correct(self):
        balance = self.client.withdraw(300)
        self.assertEqual(balance, 700)

    def test_withdraw_negative_amount(self):
        with self.assertRaises(ValueError):
            self.client.withdraw(-300)

    def test_withdraw_incorrect_type(self):
        with self.assertRaises(TypeError):
            self.client.withdraw("aa")

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.client.withdraw(2000)


    def test_deposit_correct(self):
        balance = self.client.deposit(300)
        self.assertEqual(balance, 1300)

    def test_deposit_incorrect_type(self):
        with self.assertRaises(TypeError):
            self.client.deposit('a')

    def test_deposit_non_positive_value(self):
        with self.assertRaises(ValueError):
            self.client.deposit(-1)



