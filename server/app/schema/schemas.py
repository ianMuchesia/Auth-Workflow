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
    
    
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes = True)
    id: str
    name: str
    created_at: datetime
    updated_at: datetime
    role:str