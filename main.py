from fastapi import FastAPI
from contracts import CreateUserRequest, CreatedUserResponse, PayUserRequest
from db import engine
from sqlalchemy.orm import Session
from models import User, Feed
from starlette import status
from fastapi import Depends
from dependencies import get_db, get_user_service, get_feed_service, get_friend_service, get_transaction_service
from services import UserService, TransactionService


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
   







