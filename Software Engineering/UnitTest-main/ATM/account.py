class Account:

    def __init__(self, account_no, pin, balance):
        self.account_no = account_no
        self.pin = pin
        self.balance = balance

    def verify_pin(self, pin):
        return self.pin == pin

    def deposit(self, amount):

        if amount <= 0:
            raise ValueError("Invalid amount")

        self.balance += amount
        return self.balance

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("Invalid amount")

        if amount > self.balance:
            raise ValueError("Insufficient balance")

        self.balance -= amount
        return self.balance

    def check_balance(self):
        return self.balance

    def change_pin(self, old_pin, new_pin):

        if self.pin != old_pin:
            raise ValueError("Wrong PIN")

        self.pin = new_pin
        return True