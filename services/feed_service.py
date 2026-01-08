from sqlalchemy.orm import Session, joinedload
from models import Feed, Transaction


class FeedService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_payment_feed(self, transaction_id: int) -> Feed:
        feed = Feed(
            feed_type="payment",
            transaction_id=transaction_id
        )
        self.db.add(feed)
        return feed
    
    def create_friend_feed(self, user_id: int, friend_id: int) -> Feed:
        feed = Feed(
            feed_type="friend_add",
            user_pay_id=user_id,
            user_paid_id=friend_id
        )
        self.db.add(feed)
        return feed
    
    def get_user_feed(self, user_id: int) -> list[Feed]:

        return self.db.query(Feed).options(
            joinedload(Feed.transaction).joinedload(Transaction.payer),
            joinedload(Feed.transaction).joinedload(Transaction.payee),
            joinedload(Feed.user_pay),
            joinedload(Feed.user_paid)
        ).filter(
            (Feed.transaction.has(Transaction.payer_id == user_id)) |
            (Feed.transaction.has(Transaction.payee_id == user_id)) |
            
            (Feed.user_pay_id == user_id) |
            (Feed.user_paid_id == user_id)
        ).order_by(Feed.created_at.desc()).all()

