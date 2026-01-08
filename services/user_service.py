from sqlalchemy.orm import Session
from models import User
from contracts import CreateUserRequest, CreatedUserResponse

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, req: CreateUserRequest):
        try:
            user = User(
                name=req.name,
                last_name=req.last_name,
                phone=req.phone,
                balance=req.balance,
                credit_debt=req.credit_debt
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            return CreatedUserResponse(
                id=user.id,
                name=user.name,
                last_name=user.last_name,
                phone=user.phone,
                balance=user.balance,
                credit_debt=user.credit_debt
            )
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_user(self, user_id: int) -> User:

        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user