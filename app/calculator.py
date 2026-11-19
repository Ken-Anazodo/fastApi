def add(num1: int, num2: int):
    return num1 + num2


def subtract(num1: int, num2: int):
    return num1 - num2


def multiply(num1: int, num2: int):
    return num1 * num2


def divide(num1: int, num2: int):
    return num1 / num2


class Insufficient_funds(Exception):
    pass


class Bank_account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise Insufficient_funds("You have Insufficient funds")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance
    
    def collect_interest(self):
        self.balance *= 1.1
        return self.balance
      

