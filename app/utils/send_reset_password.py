from .send_email import send_email

async def send_reset_password_email(name:str, email:str, token:str,origin:str):
    reset_url = f"{origin}/auth/reset-password?token={token}&email={email}"
    
    html = f"""
    <html>
        <body>
            <p>Hi {name},</p><br>
            <p>Click the link below to reset your password</p><br>
            <a href="{reset_url}" style="color:blue">Reset Password Here</a>
        </body>
    </html>
    
    """
    
    await send_email(
     email=email,
     subject="Reset Password",
    html=html
    )