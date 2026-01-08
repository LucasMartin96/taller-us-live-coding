from sqlalchemy.orm import Session, joinedload
from models import Feed, Transaction
from contracts import GetFeedResponse, GetAllFeedResponse


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
            payer_id=user_id,
            payee_id=friend_id
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
            
            (Feed.payer_id == user_id) |
            (Feed.payee_id == user_id)
        ).order_by(Feed.created_at.desc()).all()
    
    def format_feed_entry(self, feed: Feed) -> GetFeedResponse:

        if feed.feed_type == "payment" and feed.transaction:
            payer_name = feed.transaction.payer.name
            payee_name = feed.transaction.payee.name
            amount = feed.transaction.amount
            description = feed.transaction.description or ""
            feed_description = f"{payer_name} paid {payee_name} ${amount:.2f} for {description}"
        
        elif feed.feed_type == "friend_add":
            feed_description = f"{feed.user_pay.name} added {feed.user_paid.name} as a friend"
        
        return GetFeedResponse(id=feed.id, feed_description=feed_description)
    
    def get_formatted_feed(self, user_id: int) -> GetAllFeedResponse:

        feeds = self.get_user_feed(user_id)
        formatted_feeds = [self.format_feed_entry(feed) for feed in feeds]
        return GetAllFeedResponse(feeds=formatted_feeds)

