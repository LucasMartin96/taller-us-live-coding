from sqlalchemy.orm import Session, joinedload
from models import Feed, Transaction

class FeedService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_feed(self, user_id: int) -> list[Feed]:

        return self.db.query(Feed).options(
            joinedload(Feed.transaction).joinedload(Transaction.payer),
            joinedload(Feed.transaction).joinedload(Transaction.payee),
            joinedload(Feed.user_pay),
            joinedload(Feed.user_paid)
        ).filter(
            (Feed.transaction.has(Transaction.payer_id == user_id)) |
            (Feed.transaction.has(Transaction.payee_id == user_id))
        ).order_by(Feed.created_at.desc()).all()
    
    
    