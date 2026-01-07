import unittest
from main import pay


class FakeUser:
    def __init__(self, balance=0.0, credit_debt=0.0, **kwargs):
        self.balance = balance
        self.credit_debt = credit_debt
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestPay(unittest.TestCase):
    def test_sufficient_balance_deducts_and_credits(self):
        payer = FakeUser(balance=100.0, credit_debt=0.0)
        payee = FakeUser(balance=50.0, credit_debt=0.0)
        pay(payer, payee, 30.0)
        self.assertEqual(payer.balance, 70.0)
        self.assertEqual(payer.credit_debt, 0.0)
        self.assertEqual(payee.balance, 80.0)

    def test_insufficient_balance_uses_credit_and_credits_payee(self):
        payer = FakeUser(balance=20.0, credit_debt=5.0)
        payee = FakeUser(balance=10.0, credit_debt=0.0)
        pay(payer, payee, 50.0)
        self.assertEqual(payer.balance, 0.0)
        self.assertEqual(payer.credit_debt, 35.0)  # 5 existing + (50 - 20)
        self.assertEqual(payee.balance, 60.0)

    def test_exact_balance_zeroes_payer_no_credit_debt(self):
        payer = FakeUser(balance=40.0, credit_debt=2.0)
        payee = FakeUser(balance=0.0, credit_debt=0.0)
        pay(payer, payee, 40.0)
        self.assertEqual(payer.balance, 0.0)
        self.assertEqual(payer.credit_debt, 2.0)
        self.assertEqual(payee.balance, 40.0)

    def test_multiple_payments_accumulate_credit_debt(self):
        payer = FakeUser(balance=30.0, credit_debt=0.0)
        payee = FakeUser(balance=0.0)
        pay(payer, payee, 20.0)  # remaining balance 10
        pay(payer, payee, 25.0)  # shortfall 15
        self.assertEqual(payer.balance, 0.0)
        self.assertEqual(payer.credit_debt, 15.0)
        self.assertEqual(payee.balance, 45.0)

    def test_zero_amount_no_changes(self):
        payer = FakeUser(balance=10.0, credit_debt=1.0)
        payee = FakeUser(balance=5.0, credit_debt=0.0)
        pay(payer, payee, 0.0)
        self.assertEqual(payer.balance, 10.0)
        self.assertEqual(payer.credit_debt, 1.0)
        self.assertEqual(payee.balance, 5.0)


if __name__ == "__main__":
    unittest.main()
