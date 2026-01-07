


class CreateUserRequest():
    name: str
    last_name: str
    phone: str
    balance: float
    credit_debt: float

class CreatedUserResponse():
    id: int
    name: str
    last_name: str
    phone: str
    balance: float
    credit_debt: float

class PayUserRequest():
    user_to_pay_id: int
    ammount: float