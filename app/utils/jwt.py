from datetime import datetime, timedelta,timezone
from fastapi import Response, Request
from jose import JWTError, jwt
from ..config.config import settings
# from ..models.models import User

def create_jwt(payload: dict):
    try:
        to_encode = payload.copy()
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        print(encoded_jwt)
        return encoded_jwt
    except JWTError:
        raise JWTError("Error encoding jwt")

def is_token_valid(token: str):
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return True
    except JWTError:
        return False

def attach_cookies_to_response(request: Request, response: Response, user, refresh_token: str):
  
    print(user)
    user_dict = {
        "userId": user["userId"],
        "name": user["name"],
        "role": user["role"],
    }
    
   

    # Create JWT tokens
    access_token_jwt = create_jwt({"user": user_dict})
    refresh_token_jwt = create_jwt({"user": user_dict, "refresh_token": refresh_token})

   
    
    one_day = (datetime.now(timezone.utc) + timedelta(days=1))
    longer_exp = (datetime.now(timezone.utc) + timedelta(days=30))

   
    response.set_cookie(
        key="accessToken",
        value=access_token_jwt,
        httponly=True,
        secure=False,
        # secure=request.url.scheme == "https",
        expires=one_day,
    )

    response.set_cookie(
        key="refreshToken",
        value=refresh_token_jwt,
        httponly=True,
        secure=False,
        # secure=request.url.scheme == "https",
        expires=longer_exp,
    )