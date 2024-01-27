import secrets
from fastapi import Request,Response
from pytz import utc

from ..models.models import User,Token
from sqlalchemy.orm import Session
from ..errors import errors
from ..utils import send_verification,hash,create_token_user,jwt,send_reset_password,create_hash

from starlette.responses import JSONResponse
from datetime import datetime,timedelta




async def create_user(user:User, db: Session,request:Request):
    
    emailExists = db.query(User).filter(User.email == user.email).first()
    
    if emailExists:
        raise errors.BadRequestError("Email already exists")
    
    #first registered is admin
    role = "admin" if db.query(User).count() == 0 else "user"
        
    verification_token = secrets.token_hex(40)
    
    hashed_password = hash.hash_password(user.password)
    
    
    # create a new User instance
    new_user = User(
        email=user.email,
        password=hashed_password, 
        name=user.name,
        role=role,
        verificationToken=verification_token,
    )
    
    
    db.add(new_user)
    
    db.commit()
    
    tempOrigin = request.headers.get("origin")
    
    await send_verification.send_verification_email(name=user.name,email=user.email,verfication_token=verification_token,origin=tempOrigin)
  
    return JSONResponse(status_code=201,content={"message":"user created successfully"})
    
    
    
    
def verify_user_email(user:User,db:Session):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise errors.NotFoundError("User not found")
    
    if db_user.verificationToken != user.verificationToken:
        raise errors.UnauthorizedError("Verification failed")
    
    db_user.isVerified = True
    db_user.verified = datetime.utcnow()
    db_user.verificationToken = ""
    
    
    db.commit()
    db.refresh(db_user)
    
    return JSONResponse(status_code=200,content={"message":"Email verified successfully"})
    
        
        
def login_user(req: Request, res: Response,user:User, db:Session):
    
    db_user = db.query(User).filter(User.email == user.email).first()
   
   
    if not db_user:
        raise errors.UnauthorizedError("Invalid Credentials")
    
    isPasswordValid = hash.verify_password(user.password,db_user.password)
    
    
    if not isPasswordValid:
        raise errors.UnauthorizedError("Invalid Credentials")
    
    if not db_user.isVerified:
        raise errors.UnauthorizedError("Email not verified")
    
    token_user = create_token_user.create_token_user(db_user)
    
    refresh_token = ''
    
    #check for existing token
    existing_token = db.query(Token).filter(Token.user == db_user.id).first()
    
    
    if existing_token:
        print("we are here in existing token")
        if not existing_token.isValid:
            raise errors.UnauthorizedError("Invalid Credentials")
        
        refresh_token = existing_token.refreshToken
        
        response = JSONResponse(status_code=200, content={"user":token_user})

        
        jwt.attach_cookies_to_response(req, response, token_user, refresh_token)
        return response
    else:
        print("we are here the new token is created ")
        refresh_token = secrets.token_hex(40)
        
        user_agent = req.headers.get("user-agent")
        client_ip = req.client.host
        print(user_agent,client_ip)
        if not user_agent or not client_ip:
            raise errors.CustomHTTPException("Client Information Access Cannot be retrieved")
        
        user_token = Token(
            refreshToken=refresh_token,
            ip=client_ip,
            userAgent=user_agent,
            user=db_user.id
            
        )
        
        db.add(user_token)
        db.commit()
        
        jwt.attach_cookies_to_response(req,res,token_user,refresh_token)
        
        return JSONResponse(status_code=200, content={"user":token_user})
        
        
def logout_user(res:Response,db:Session, user):
    
    #delete the token from the database
    print(user)
    db_token = db.query(Token).filter(Token.user == user["userId"]).first()
    
    if not db_token:
        raise errors.NotFoundError("Token not found")
    db.delete(db_token)
    
    db.commit()
    
    response = JSONResponse(status_code=200,content={"message":"Logged out successfully"})
    #delete the cookies
    response.delete_cookie("accessToken")
    response.delete_cookie("refreshToken")

    
    return response



async def forgot_password (req:Request,email:str,db:Session):
    
    db_user = db.query(User).filter(User.email == email).first()
    
    if not db_user:
        raise errors.NotFoundError("User not found")
    
    if not db_user.isVerified:
        raise errors.UnauthorizedError("Email not verified")
    
    #generate a token
    token = secrets.token_hex(70)

    origin = req.headers.get("origin")
    if not origin:
        raise errors.BadRequestError("Origin not found")
    #send the email
    print(origin)
    await send_reset_password.send_reset_password_email(name=db_user.name,email=db_user.email,token=token,origin=origin)
        
    # ten_minutes = datetime.utcnow() + timedelta(minutes=10)
    
    # password_expiration_date = datetime.utcnow() + ten_minutes
    
    ten_minutes = timedelta(minutes=10)
    password_expiration_date = datetime.utcnow().replace(tzinfo=utc) + ten_minutes
    
    #save the token in the database
    db_user.passwordToken = create_hash.hash_string(token)
    db_user.passwordTokenExpires = password_expiration_date
    
    db.commit()
    db.refresh(db_user)
    
    return JSONResponse(status_code=201,content={"message":"Reset token created successfully"})
    
    
    
def reset_password(user:User,db:Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise errors.NotFoundError("User not found")
    
     
    current_date = datetime.utcnow().replace(tzinfo=utc)
    
  
    print(db_user.passwordTokenExpires)
    if current_date > db_user.passwordTokenExpires:
        raise errors.UnauthorizedError("Token expired")
    
    if not db_user.isVerified:
        raise errors.UnauthorizedError("Email not verified")
    
    
    if db_user.passwordToken != create_hash.hash_string(user.passwordToken):
        raise errors.UnauthorizedError("Invalid Credentials")
    
    
    hashed_password = hash.hash_password(user.password)
    
    db_user.password = hashed_password
    
    db.commit()
    db.refresh(db_user)
    
    return JSONResponse(status_code=201,content={"message":"Password reset successfully"})
   