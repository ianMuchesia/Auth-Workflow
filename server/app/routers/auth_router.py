from fastapi import APIRouter,Request,Depends,Response
from ..database.db import get_db
from sqlalchemy.orm import Session
from ..controllers.auth_controller import create_user,verify_user_email,login_user
from ..schema.schemas import UserCreate,UserVerify,UserLogin
from ..middlewares.authenticate_user import authenticate_user as auth







router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    
)



@router.post("/register")
async def register_user(user:UserCreate, request:Request,db:Session=Depends(get_db)):
    return await create_user(user=user,db=db, request=request)
    
    
    
@router.post("/verify-email")
def verify_email(user:UserVerify,db:Session=Depends(get_db)):
    return verify_user_email(user,db)


@router.post("/login")
def login(req:Request, res:Response, user:UserLogin, db:Session=Depends(get_db)):
    return login_user(req,res,user,db)


@router.get("/me")
def show_me(user=Depends(auth)):
    return {"message":"Hello World"}