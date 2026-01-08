import unittest
from services.payment_service import PaymentService


class FakeUser:
    def __init__(self, balance=0.0, credit_debt=0.0):
        self.balance = balance
        self.credit_debt = credit_debt


class TestPaymentService(unittest.TestCase):
    def test_sufficient_balance_uses_only_balance(self):
        payer = FakeUser(balance=100.0, credit_debt=0.0)
        payee = FakeUser(balance=50.0, credit_debt=0.0)
        
        PaymentService().execute_payment(payer, payee, 30.0)
        
        self.assertEqual(payer.balance, 70.0)
        self.assertEqual(payer.credit_debt, 0.0)
        self.assertEqual(payee.balance, 80.0)
    
    def test_insufficient_balance_uses_credit(self):
        payer = FakeUser(balance=20.0, credit_debt=5.0)
        payee = FakeUser(balance=10.0, credit_debt=0.0)
        
        PaymentService().execute_payment(payer, payee, 50.0)
        
        self.assertEqual(payer.balance, 0.0)
        self.assertEqual(payer.credit_debt, 35.0)
        self.assertEqual(payee.balance, 60.0)
    
    def test_calculate_payment_split_sufficient_balance(self):
        payer = FakeUser(balance=100.0, credit_debt=0.0)
        
        balance_used, credit_used = PaymentService().calculate_payment_split(payer, 30.0)
        
        self.assertEqual(balance_used, 30.0)
        self.assertEqual(credit_used, 0.0)
    
    def test_calculate_payment_split_insufficient_balance(self):
        payer = FakeUser(balance=20.0, credit_debt=5.0)
        
        balance_used, credit_used = PaymentService().calculate_payment_split(payer, 50.0)
        
        self.assertEqual(balance_used, 20.0)
        self.assertEqual(credit_used, 30.0)


if __name__ == "__main__":
    unittest.main()
