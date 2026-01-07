from fastapi import FastAPI
from contracts import CreateUserRequest, CreatedUserResponse, PayUserRequest
from db import engine
from sqlalchemy.orm import Session
from models import User, Feed
from starlette import status
from fastapi import Depends
from dependencies import get_db


app = FastAPI()



@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(req: CreateUserRequest, db: Session = Depends(get_db)) -> CreatedUserResponse:
    user = User(name=req.name, last_name=req.last_name, phone=req.phone, balance=req.balance)  

    db.add(user)
    db.commit()
    db.refresh(user)
    response = CreatedUserResponse(id= user.id, last_name=user.last_name, phone=user.phone, balance=user.balance, credit_debt=user.credit_debt)
    return response

@app.post("/user-payment", status_code=status.HTTP_200_OK)
def pay_user(req: PayUserRequest):
    # Lets asume i have a token and i can get the user from jwt

    with Session(engine) as session:
        paying_user = session.get(User, 1)
        user_to_pay = session.get(User, req.user_to_pay_id)
        pay(paying_user, user_to_pay, req.ammount)

        session.add(Feed(user_pay_id= paying_user.id, user_paid_id= user_to_pay.id, ammount=req.ammount))

        session.commit()
    

@app.get("/feed", status_code=status.HTTP_200_OK)
def get_feed():
    # Lets asume i have a token and i can get the user from jwt
    user_id = 1

    with Session(engine) as session:
        




def pay(paying_user: User, user_to_pay: User, ammount):
    if paying_user.balance >= ammount:
        paying_user.balance -= ammount
        return 
    credit_card_ammount = paying_user.balance - ammount
    paying_user.balance = 0
    paying_user.credit_debt += credit_card_ammount
    user_to_pay.balance += ammount






