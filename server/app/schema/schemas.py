from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    name: str
    email: EmailStr
    
    

class UserCreate(UserBase):
    password: str
    name: str
    email: EmailStr
    phone: str
    role:Optional[str] = "user"
    verificationToken: Optional[str] = None 
    
    
class UserVerify(BaseModel):
    email: EmailStr
    verificationToken: str
    
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes = True)
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    role:str
    
    
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class UserForgotPassword(BaseModel):
    email:EmailStr
    
class UserResetPassword(BaseModel):
    password:str
    passwordToken:str
    email:EmailStr