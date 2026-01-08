from typing import Tuple
from models import User


class PaymentService():
    def calculate_payments_credit_balance(self, payer : User, ammount: float):
        balance_use = min(payer.balance, ammount)
        credit_use = max(0.0, ammount - payer.balance)
        return balance_use, credit_use
    

    
