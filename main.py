from fastapi import FastAPI
from contracts import AddFriendResponse, CreateUserRequest, CreatedUserResponse, GetAllFeedResponse, PayUserRequest, TransactionResponse
from starlette import status
from fastapi import Depends
from dependencies import get_user_service, get_feed_service, get_friend_service, get_transaction_service
from services import UserService, TransactionService, FeedService, FriendService 
from fastapi import HTTPException

app = FastAPI()

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    req: CreateUserRequest,
    user_service: UserService = Depends(get_user_service)
) -> CreatedUserResponse:
    try:

        result =  user_service.create_user(req)
        
        return CreatedUserResponse.model_validate({
            "id": result.id,
            "name": result.name,
            "last_name": result.last_name,
            "phone": result.phone,
            "balance": result.balance,
            "credit_debt": result.credit_debt
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions", status_code=status.HTTP_200_OK)
def pay_user(
    req: PayUserRequest,
    user_service: UserService = Depends(get_user_service),
    transaction_service: TransactionService = Depends(get_transaction_service)
) -> TransactionResponse:
    try:
        paying_user = user_service.get_user(1)
        user_to_pay = user_service.get_user(req.user_to_pay_id)
        
        transaction = transaction_service.create_payment_transaction(
            payer=paying_user,
            payee=user_to_pay,
            amount=req.ammount,
            description=req.description
        )
        
        return TransactionResponse.model_validate({
            "transaction_id": transaction.id,
            "payer_id": transaction.payer_id,
            "payee_id": transaction.payee_id,
            "amount": transaction.amount,
            "description": transaction.description or ""
        })
    except ValueError as e:
        if "not found" in str(e).lower(): # Here it would be better to have custom exceptions. Same for simplicty i left it like this.
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   
@app.get("/users/{user_id}/feed", status_code=status.HTTP_200_OK)
def get_feed(
    user_id: int,
    feed_service: FeedService = Depends(get_feed_service)
) -> GetAllFeedResponse:
    try:
        return feed_service.get_formatted_feed(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/users/{user_id}/friends", status_code=status.HTTP_200_OK)
def add_friend(
    user_id: int,
    friend_id: int,
    friend_service: FriendService = Depends(get_friend_service)
) -> AddFriendResponse:
    try:
        friend_service.add_friend(user_id, friend_id)
        return AddFriendResponse(
            user_id=user_id,
            friend_id=friend_id,
            message="Friend added successfully"
        )
    except ValueError as e:
        if "not found" in str(e).lower(): # Here it would be better to have custom exceptions.
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



