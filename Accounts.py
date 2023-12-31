from Exceptions import *

class Accounts():

    def __init__(self, account_id, username, password, currency, balance):
        self.account_id = account_id
        self.username = username
        self.password = password
        self.currency = self.validate_Currency(currency)
        self.balance = self.validate_Amount(balance)

    def validate_Currency(self, currency):
        currencies = ["EUR", "USD", "AUD", "JPY", "GBP"]
        if currency.upper() not in currencies:
            return AbortTransaction("Currency type is wrong")
        return currency.upper()
        
        
    def validate_Amount(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            raise AbortTransaction("Amount must be a number: integer or float")
        if amount < 0:
            raise AbortTransaction("Amount can not be negative")
        return amount

    def check_password_match(self, password):
        if password != self.password:
            raise AbortTransaction("Incorrect password for this account")
        
    def deposit(self, amount_to_deposit):
        amount_to_deposit = self.validate_Amount(amount_to_deposit)
        self.balance = self.balance + amount_to_deposit
        return self.balance
    
    def get_balance(self):
        return self.balance
    
    def get_currency(self):
        return self.currency

    def withdraw(self, amount_to_withdraw):
        amount_to_withdraw = self.validate_Amount(amount_to_withdraw)
        if amount_to_withdraw > self.balance:
            raise AbortTransaction("You cant withdraw more than your balance")
        self.balance = self.balance - amount_to_withdraw
        return self.balance
    
    def transfer_to(self, amount_to_transfer):
        amount_to_transfer = self.validate_Amount(amount_to_transfer)
        if amount_to_transfer > self.balance:
            raise AbortTransaction("You cant transfer more than your balance")
        self.balance = self.balance - amount_to_transfer
        return self.balance

    def show(self):
        print("- Account ID :", self.account_id)
        print("- Name :", self.username)
        print("- Balance :", self.balance)
        print("- Currency :", self.currency)