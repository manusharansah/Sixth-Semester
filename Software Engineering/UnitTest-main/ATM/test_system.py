import unittest
from account import Account
from atm import ATM

class TestATMSystem(unittest.TestCase):

    def test_cash_withdrawal_scenario(self):
        atm = ATM()
        acc = Account("A101", "1234", 1000)

        atm.login(acc, "1234")
        atm.withdraw_cash(acc, 500)

        self.assertEqual(atm.check_balance(acc), 500)

    def test_deposit_scenario(self):
        atm = ATM()
        acc = Account("A101", "1234", 1000)

        atm.login(acc, "1234")
        atm.deposit_cash(acc, 1000)

        self.assertEqual(atm.check_balance(acc), 2000)

    def test_pin_change_scenario(self):
        atm = ATM()
        acc = Account("A101", "1234", 1000)

        atm.login(acc, "1234")
        atm.change_pin(acc, "1234", "9999")

        self.assertTrue(acc.verify_pin("9999"))



if __name__ == "__main__":
    unittest.main()