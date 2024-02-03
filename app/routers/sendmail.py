from typing import List

from fastapi import APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from ..config.config import settings


router = APIRouter(
    prefix="/email",
    tags=["email"]
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
   MAIL_USERNAME=settings.EMAIL_USERNAME,
   MAIL_PASSWORD=settings.EMAIL_PASSWORD ,
   MAIL_FROM=settings.EMAIL_USERNAME,
   MAIL_PORT=settings.EMAIL_PORT,
   MAIL_SERVER=settings.EMAIL_SERVER,
   MAIL_FROM_NAME="Auth Work Flow",
   MAIL_STARTTLS=False,
   MAIL_SSL_TLS=True,
   USE_CREDENTIALS=True,
   VALIDATE_CERTS=True,
  
)




html = """
<p style="color:red;">Thanks for using Fastapi-mail</p> 
"""


@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.model_dump().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     