from typing import Tuple
from models import User


class PaymentService():
    def calculate_payments_credit_balance(self, user_to_pay: User, ammount: float):
        balance_use = min(user_to_pay.balance, ammount)
        credit_use = max(0.0, ammount - user_to_pay.balance)
        return balance_use, credit_use
    
    