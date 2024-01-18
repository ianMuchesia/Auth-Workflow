from .send_email import send_email

async def send_verification_email(name:str,email:str,verfication_token:str,origin:str):
    
    
    verify_email = f"{origin}/auth/verify-email?token={verfication_token}&email={email}"
    
    html_message = f"""
    <html>
        <body>
            <p>Hi {name},</p><br>
            <p>Thank you for registering in our website.</p>
            <p>Please click the link below to verify your email address.</p>
            <a href="{verify_email}">Verify Email</a>
        </body>
    </html>
    """
    
    await send_email(email=email,subject="Verify Email",html=html_message)