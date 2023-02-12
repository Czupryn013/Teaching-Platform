import os
import smtplib

from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

load_dotenv()
secret_key, salt, email_pwd, email_login = os.getenv("secret_key"),os.getenv("salt"),os.getenv("email_password"), os.getenv("email_login")


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    email = serializer.loads(token,salt=salt,max_age=expiration)
    print(email)
    if not email: return False

    return email

def send_email(to, subject, body):
    SMTP_SERVER = "smtp-mail.outlook.com"
    SMTP_PORT = 587

    message = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(email_login, to, subject, body)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_login, email_pwd)
    server.sendmail(email_login, [to], message)
    server.quit()