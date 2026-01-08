from sqlalchemy.orm import Session
from models import Transaction, User
from services.payment_service import PaymentService


class TransactionService:
    def __init__(self, db: Session, payment_service: PaymentService = None):
        self.db = db
        self.payment_service = payment_service or PaymentService()
    
    def create_payment_transaction(
        self, 
        payer: User, 
        payee: User, 
        amount: float,
        description: str = ""
    ):
        try:
            balance_used, credit_used = self.payment_service.calculate_payment_split(payer, amount)
            
            self.payment_service.execute_payment(payer, payee, amount)
            
            transaction = Transaction(
                payer_id=payer.id,
                payee_id=payee.id,
                amount=amount,
                description=description,
                balance_used=balance_used,
                credit_used=credit_used
            )
            self.db.add(transaction)
            self.db.flush() 
            
            # TODO: Create payment feed HERE. Create services for it
            
            self.db.commit()
            return transaction
        except Exception as e:
            self.db.rollback()
            raise

