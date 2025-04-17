import random

from flask_mail import Message

from app import mail


def generate_verification_code(length=6):
    """Generate a random numeric verification code."""
    return "".join(random.choices("0123456789", k=length))


def send_verification_email(user_email, code):
    """Send a verification code to the user's email."""
    msg = Message("Your Verification Code", recipients=[user_email])
    msg.body = f"Your verification code is: {code}\nPlease use it to complete the process."

    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
