from db import SessionLocal
from services import UserService, TransactionService, FeedService, FriendService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_transaction_service(db: Session = Depends(get_db)) -> TransactionService:
    return TransactionService(db)

def get_feed_service(db: Session = Depends(get_db)) -> FeedService:
    return FeedService(db)

def get_friend_service(db: Session = Depends(get_db)) -> FriendService:
    return FriendService(db)