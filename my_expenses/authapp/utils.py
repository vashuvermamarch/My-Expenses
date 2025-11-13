import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    """Generate a random 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp, purpose="Verification"):
    """Send OTP email"""
    subject = f"{purpose} OTP from MyExpenses"
    message = f"Your One-Time Password (OTP) for {purpose.lower()} is: {otp}\nIt will expire in 10 minutes."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
