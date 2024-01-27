from fastapi import Response,Request
from ..models.models import User
from sqlalchemy.orm import Session
from ..errors import errors
from ..utils import jwt as jwtmodule
from ..utils import create_token_user
from ..utils import hash
from starlette.responses import JSONResponse



def update_user(user:User, db:Session,req:Request):

    user_exists = db.query(User).filter(User.email == user.email).first()
    
    if not user_exists:
        raise errors.NotFoundError("User not found")
    
    user_exists.name = user.name
    user_exists.email = user.email
    
    db.commit()
    
    db.refresh(user_exists)
    
    response = JSONResponse (status_code=200,content={"message":"user updated successfully"})
    
    token_user = create_token_user.create_token_user(user_exists)
    jwtmodule.attach_cookies_to_response(req,response,token_user,"")
    
    return response


def update_user_password(user:User,old_password,new_password,db:Session):
    user_exists = db.query(User).filter(User.email == user.email).first()
    
    if not user_exists:
        raise errors.NotFoundError("User not found")
    
    isPasswordValid = hash.verify_password(old_password,user_exists.password)
    
    if not isPasswordValid:
        raise errors.ForbiddenError("Invalid Credentials")
    
    user_exists.password = hash.hash_password(new_password)
    
    db.commit()
    
    db.refresh(user_exists)

    return JSONResponse(status_code=200,content={"message":"Password updated successfully"})    
    
    
 