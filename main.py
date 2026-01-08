from fastapi import FastAPI
from contracts import CreateUserRequest, CreatedUserResponse, PayUserRequest
from db import engine
from sqlalchemy.orm import Session
from models import User, Feed
from starlette import status
from fastapi import Depends
from dependencies import get_db, get_user_service, get_feed_service, get_friend_service, get_transaction_service
from services import UserService


app = FastAPI()



@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(req: CreateUserRequest, user_service: UserService = Depends(get_user_service)) -> CreatedUserResponse:

    response = user_service.create_user(req)

    return response

@app.post("/user-payment", status_code=status.HTTP_200_OK)
def pay_user(req: PayUserRequest):
    pass
    

@app.get("/feed", status_code=status.HTTP_200_OK)
def get_feed():
    # Lets asume i have a token and i can get the user from jwt
    user_id = 1

    pass







