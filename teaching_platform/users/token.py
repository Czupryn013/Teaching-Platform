import os

from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from teaching_platform.extensions import mail

load_dotenv()
secret_key, salt = os.getenv("secret_key"),os.getenv("salt")


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    email = serializer.loads(token,salt=salt,max_age=expiration)
    if not email: return False

    return email

def send_email(to, subject, html):
    msg = Message(subject, html=html, recipients=[to], sender="CryptoCharts09@gmail.com")
    mail.send(msg)