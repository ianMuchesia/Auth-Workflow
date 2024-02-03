from fastapi import Depends, Request, Response
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..utils import jwt as jwtmodule
from jose import jwt
from ..config.config import settings
from ..errors import errors


def authenticate_user(req: Request, res: Response, db: Session = Depends(get_db)):
    access_token = req.cookies.get("accessToken")
    refresh_token = req.cookies.get("refreshToken")

    # print(req.cookies)
    if not access_token and not refresh_token:
        raise errors.UnauthorizedError("Access Forbidden")

    if access_token:
        is_valid = jwtmodule.is_token_valid(access_token)
        # print(is_valid)
        if is_valid:
            access_token_decoded = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user = access_token_decoded.get("user")
            return user
        else:
            raise errors.UnauthorizedError("Invalid token")

    if refresh_token:
        is_valid = jwtmodule.is_token_valid(refresh_token)
        if is_valid:
          
            refresh_token_decoded = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user = refresh_token_decoded.get("user")
            
           
            
            refresh_token = refresh_token_decoded.get("refresh_token")
            # print(refresh_token)
            jwtmodule.attach_cookies_to_response(req, res, user, refresh_token)
            return user
        else:
            raise errors.UnauthorizedError("Invalid token")