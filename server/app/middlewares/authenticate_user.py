from fastapi import Depends, Request, Response
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..utils import jwt
from ..config.config import settings
from ..errors import errors


def authenticate_user(req: Request, res: Response, db: Session = Depends(get_db)):
    access_token = req.cookies.get("accessToken")
    refresh_token = req.cookies.get("refreshToken")

    print(req.cookies)
    if not access_token and not refresh_token:
        raise errors.UnauthorizedError("No token provided")

    if access_token:
        is_valid = jwt.is_token_valid(access_token)
        if is_valid:
            return True
        else:
            raise errors.UnauthorizedError("Invalid token")

    if refresh_token:
        is_valid = jwt.is_token_valid(refresh_token)
        if is_valid:
            refresh_token_decoded = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user = refresh_token_decoded.get("user")
            refresh_token = refresh_token_decoded.get("refresh_token")
            jwt.attach_cookies_to_response(req, res, user, refresh_token)
            return True
        else:
            raise errors.UnauthorizedError("Invalid token")