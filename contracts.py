from pydantic import BaseModel


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