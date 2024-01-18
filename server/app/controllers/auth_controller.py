import secrets
from fastapi import Request
from ..models.models import User
from sqlalchemy import Session
from ..errors import errors
from ..utils import send_verification
from starlette.responses import JSONResponse





async def create_user(user:User, db: Session,request:Request):
    
    emailExists = db.query(User).filter(User.email == user.email).first()
    
    if emailExists:
        raise errors.BadRequestError("Email already exists")
    
    #first registered is admin
    if db.query(User).count() == 0:
        user.role = "admin"
    else:
        user.role = "user"
        
    verificationToken = secrets.token_hex(40)
    
    
    user.verification_token = verificationToken
    
    db.add(user)
    
    db.commit()
    
    tempOrigin = request.headers.get("origin")
    
    await send_verification.send_verification_email(name=user.name,email=user.email,verfication_token=verificationToken,origin=tempOrigin)
    
    
    return JSONResponse(status_code=201,content={"message":"user created successfully"})
    
    
    
    
    
        
    
    
        