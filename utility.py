from pydantic import BaseModel
from typing import Optional
class Signup(BaseModel):
    username : str
    email : str
    password : str
    is_staff : Optional[bool] = False
    is_active : Optional[bool] = False
    

class SignupResponse(BaseModel):
    username : str 
    email : str
    password : str
    
    class config:
        orm_mode = True
        schema_extra = {
            'example':{
                "username":"adekunleabioye",
                "email" : "adekunleabioye@gmail.com",
                "password" : "password"
            }
        }
    
class TokenData(BaseModel):
    id : Optional[int] = None
    
class Login(BaseModel):
    username : str
    password : str
    
class OrderModel(BaseModel):
    quantity : int
    order_status : Optional[str] = 'PENDING'
    pizza_size : Optional[str] = 'SMALL'
    
class OrderModels(BaseModel):
    quantity : int
    order_status : Optional[str] = 'PENDING'
    pizza_size : Optional[str] = 'SMALL'
    user_id : int


    
class OrderStatus(BaseModel):
    order_status : Optional[str] = 'PENDING'
    class config:
        orm_mode = True
        schemas_extra = {
            "example": {
                "order_status" : "PENDING"
            }
        }
