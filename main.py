from fastapi import FastAPI
from contracts import CreateUserRequest, CreatedUserResponse, PayUserRequest
from db import engine
from sqlalchemy.orm import Session
from models import User, Feed
from starlette import status
from fastapi import Depends
from dependencies import get_db, get_user_service, get_feed_service, get_friend_service, get_transaction_service
from services import UserService, TransactionService, FeedService, FriendService


app = FastAPI()



@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(req: CreateUserRequest, user_service: UserService = Depends(get_user_service)) -> CreatedUserResponse:

    response = user_service.create_user(req)

    return response

@app.post("/transactions", status_code=status.HTTP_200_OK)
def create_transaction(req: PayUserRequest, user_service: UserService = Depends(get_user_service), transactions_service: TransactionService = Depends(get_transaction_service)):
    payer = user_service.get_user(1)
    payee = user_service.get(req.user_to_pay_id)

    transactions_service.create_payment_transaction(payer, payee, req.ammount, description=req.description)

    return {"result": "success"}
   
@app.get("/users/{user_id}/feed", status_code=status.HTTP_200_OK)
def get_feed(user_id: int,feed_service: FeedService = Depends(get_feed_service)):
    return feed_service.get_user_feed(user_id)


@app.post("/users/{user_id}/friends", status_code=status.HTTP_200_OK)
def add_friend(
    user_id: int,
    friend_id: int,
    friend_service: FriendService = Depends(get_friend_service)
):
    return friend_service.add_friend(user_id, friend_id)



