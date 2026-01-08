from sqlalchemy.orm import Session
from services.user_service import UserService
from services.feed_service import FeedService


class FriendService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.feed_service = FeedService(db)
    
    def add_friend(self, user_id: int, friend_id: int) -> None:
        try:
            user = self.user_service.get_user(user_id)
            friend = self.user_service.get_user(friend_id)
            
            if friend in user.friends:
                raise ValueError("Users are already friends")
            
            user.friends.append(friend)
            
            self.feed_service.create_friend_feed(user.id, friend.id)
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise

