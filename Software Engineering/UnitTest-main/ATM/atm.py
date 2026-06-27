class ATM:

    def login(self, account, pin):

        if account.verify_pin(pin):
            return "Login Successful"

        raise ValueError("Invalid PIN")

    def deposit_cash(self, account, amount):
        return account.deposit(amount)

    def withdraw_cash(self, account, amount):
        return account.withdraw(amount)

    def check_balance(self, account):
        return account.check_balance()

    def change_pin(self, account, old_pin, new_pin):
        return account.change_pin(old_pin, new_pin)