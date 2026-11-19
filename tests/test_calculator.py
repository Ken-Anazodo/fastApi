import pytest
from app.calculator import add, subtract, divide, multiply, Bank_account, Insufficient_funds
from pytest import fixture

    
def test_subtract():
    assert subtract(5, 3) == 2 #assert is used to throw an error if the condition isn't met. 
    
def test_multiply():
    assert multiply(5, 3) == 15
    
def test_divide():
    assert divide(10, 2) == 5
    
#===============================================================================================
"""Using Parametrize"""
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (1, 1, 2),
    (0, 0, 0),
]) 

def test_add(a, b, expected):
    assert add(a, b) == expected  
    

#======================================================================================= 
"""Using Parametrize with the test_get_balance function to test Bank_account class"""
@pytest.mark.parametrize("amount", [
    (1000),
    (2000),
    (5000),
] )
    
def test_get_balance(amount):
    acct_bal = Bank_account(amount)
    assert acct_bal.get_balance() == amount
#========================================================================

"""Using Fixture"""
@pytest.fixture #it's a function that runs before a test runs. fixture is used to create a reusable object. it is passed as a parameter in the test function. example: instead of initializing or creating new instance Bank_account in all our test function, we instead reuse the fixture bank_ account in the parameter of the test function where we needed to create an instance of Bank_account to have a bank "balance"   
def bank_account():
    return Bank_account(1000)

@pytest.fixture
def zero_bank_account():
    print("Creating empty Bank account")
    return Bank_account()
    
def test_set_initial_amount(bank_account):
    assert bank_account.get_balance() == 1000
    
def test_bank_default_amount(zero_bank_account):
    print("testing my bank account")
    assert zero_bank_account.get_balance() == 0
    
def test_deposit(bank_account):
    bank_account.deposit(500)
    assert bank_account.get_balance() == 1500

def test_withdraw(bank_account):
    bank_account.deposit(1000)
    bank_account.withdraw(500)
    assert bank_account.get_balance() == 1500
    
def test_collect_interest(bank_account):
    assert round(bank_account.collect_interest(), 6) == 1100
#=======================================================================================    

"""Combining Fixtures and Parametrize"""    
@pytest.mark.parametrize("deposit, withdraw, expected", [
    (1000, 500, 500),
    (2000, 1000, 1000),
    (5000, 2000, 3000),
])
def test_bank_transaction_param(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.get_balance() == expected
    

"""Testing Exceptions"""
def test_withdraw_insufficient_funds(bank_account):
    with pytest.raises(Insufficient_funds): #pytest.raises is used in our test to test if an exception is raised and true for the type of exception we expect. it's best practice to define the type of exception you are expecting rather than using general Exception. For example Insufficient_funds is defined in calculator.py module and extends the Exception class, if the withdraw method throws a different type of exception other than Insufficient_funds that it expects then this test_withdraw_insufficient_funds() function fails. 
        bank_account.withdraw(2000)
   

 
    
