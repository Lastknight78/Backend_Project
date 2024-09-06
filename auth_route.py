from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import Signup, SignupResponse
from database import get_db
from models import User
import utility, auth
auth_router = APIRouter(
    prefix='/auth',
    tags = ['auth']
)

@auth_router.get('/')
async def hello():
    return {"message":"hello world"}



@auth_router.post("/signup",response_model= SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(users : Signup,db : Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == users.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='User with this email exists')
    db_username = db.query(User).filter(User.username == users.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='User with this username exists')
    hashed_password = utility.hash(users.password)
    users.password = hashed_password
    new_user = User(**users.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    


@auth_router.post("/login")
def login(user_credentials : OAuth2PasswordRequestForm=Depends(), db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utility.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = auth.create_access_token(data={"user_id":user.id})
    return {"access_token" : access_token, "token_type":"bearer"}
