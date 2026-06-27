import unittest
from atm import ATM
from account import Account

class TestATMIntegration(unittest.TestCase):

    def setUp(self):
        self.atm = ATM()
        self.acc = Account("A101", "1234", 1000)

    def test_login_and_balance(self):

        self.atm.login(self.acc, "1234")

        self.assertEqual(
            self.atm.check_balance(self.acc),
            1000
        )

    def test_deposit_and_balance(self):

        self.atm.deposit_cash(
            self.acc,
            500
        )

        self.assertEqual(
            self.atm.check_balance(self.acc),
            1500
        )

    def test_withdraw_and_balance(self):

        self.atm.withdraw_cash(
            self.acc,
            300
        )

        self.assertEqual(
            self.atm.check_balance(self.acc),
            700
        )

if __name__ == "__main__":
    unittest.main()        
