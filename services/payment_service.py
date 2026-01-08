from typing import Tuple
from models import User


class PaymentService():
    def calculate_payment_split(self, payer : User, amount: float):
        balance_use = min(payer.balance, amount)
        credit_use = max(0.0, amount - payer.balance)
        return balance_use, credit_use
    
    def execute_payment(self, payer: User, payee, amount: float):
        payee.balance += amount
        
        if payer.balance >= amount:
            payer.balance -= amount
            return
        
        credit_card_amount = amount - payer.balance
        payer.balance = 0
        payer.credit_debt += credit_card_amount # I assume this is credit card debt without limits

    
