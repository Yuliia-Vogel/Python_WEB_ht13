import os
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from dotenv import load_dotenv

from src.services.auth import auth_service

load_dotenv() # завантажуються дані з файлу .env 

mail_username = os.getenv("MAIL_USERNAME_ENV")
mail_password = os.getenv("MAIL_PASSWORD_ENV")
mail_from = os.getenv("MAIL_FROM_ENV")
mail_server = os.getenv("MAIL_SERVER_ENV")
mail_from_name = os.getenv("MAIL_FROM_NAME_ENV")

conf = ConnectionConfig(
    MAIL_USERNAME=mail_username,
    MAIL_PASSWORD=mail_password,
    MAIL_FROM=mail_from,
    MAIL_PORT=465,
    MAIL_SERVER=mail_server,
    MAIL_FROM_NAME=mail_from_name,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)
