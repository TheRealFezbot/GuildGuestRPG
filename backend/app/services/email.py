import resend
from app.core.config import settings

resend.api_key = settings.resend_api_key

def send_verification_email(to_email, token):
    url = "http://localhost:5173/auth/verify?token=" + token
    
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": "Verify your email",
        "html": f"<p>Click <a href='{url}'>here</a> to verify your email.</p>"
    })

def send_reset_email(to_email, token):
    url = "http://localhost:8000/auth/reset-password?token=" + token

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": "Reset your password",
        "html": f"<p>Click <a href='{url}'>here</a> to reset your password.</p>"
    })