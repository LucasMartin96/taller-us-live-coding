from pydantic import BaseModel
from typing import Union

class CreateUserRequest(BaseModel):
    name: str
    last_name: str
    phone: str
    balance: float
    credit_debt: float

class CreatedUserResponse(BaseModel):
    id: int
    name: str
    last_name: str
    phone: str
    balance: float
    credit_debt: float

class PayUserRequest(BaseModel):
    user_to_pay_id: int
    ammount: float
    description: str

class TransactionResponse(BaseModel):
    transaction_id: int
    payer_id: int
    payee_id: int
    amount: float
    description: str

class GetFeedResponse(BaseModel):
    id: int
    feed_description: Union[str, None] = None

class GetAllFeedResponse(BaseModel):
    feeds: list[GetFeedResponse]

class AddFriendResponse(BaseModel):
    user_id: int
    friend_id: int
    message: str