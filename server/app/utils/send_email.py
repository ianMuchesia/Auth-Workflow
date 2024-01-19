from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse
from ..config.config import settings


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



async def send_email(email:str,subject:str,html:str):
    
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return None
    # return JSONResponse(status_code=200, content={"message": "email has been sent"})