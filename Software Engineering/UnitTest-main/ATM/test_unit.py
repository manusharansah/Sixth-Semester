import unittest
from account import Account

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.acc = Account("A101", "1234", 1000)

    def test_deposit(self):
        self.assertEqual(
            self.acc.deposit(500),
            1500
        )

    def test_withdraw(self):
        self.assertEqual(
            self.acc.withdraw(300),
            700
        )

    def test_balance(self):
        self.assertEqual(
            self.acc.check_balance(),
            1000
        )

    def test_change_pin(self):
        self.assertTrue(
            self.acc.change_pin("1234", "5678")
        )

    def test_invalid_withdraw(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(2000)


if __name__ == "__main__":
    unittest.main()            