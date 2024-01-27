from fastapi import APIRouter,Request,Depends
from ..database.db import get_db
from sqlalchemy.orm import Session
from ..schema import schemas
from ..controllers import user_controller
from ..middlewares.authenticate_user import authenticate_user as auth



router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.patch("/update")
def update_user(req:Request,user:schemas.UserUpdate,db:Session=Depends(get_db),user_present=Depends(auth)):
   
    return user_controller.update_user(user,user_present["userId"],db,req)


@router.patch("/update-password")
def update_user_password(user:schemas.UserUpdatePassword,user_present=Depends(auth),db:Session=Depends(get_db)):
    return user_controller.update_user_password(user_present["userId"],user.old_password,user.new_password,db)