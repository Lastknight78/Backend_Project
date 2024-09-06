from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas,auth_route
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oatth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
algorithm = "HS256"
access_token_expire_minute = 30

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minute)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm = algorithm)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        id : int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data

  
def get_current_user(token : str = Depends(oatth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)
