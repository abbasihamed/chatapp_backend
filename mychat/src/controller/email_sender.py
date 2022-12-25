from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import BackgroundTasks
from mychat.src.schemas.users_sc import EmailSchema


conf = ConnectionConfig(
    MAIL_USERNAME="hamed137881@gmail.com",
    MAIL_PASSWORD="bccdaweljwghhfau",
    MAIL_FROM="hamed137881@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


def send_email_verify(background_task: BackgroundTasks, emails: EmailSchema, verify_code: int):
    message = MessageSchema(
        subject="Do Not Replay",
        recipients=emails.dict().get('email'),
        body=f"کاربر گرامی کد احراز هویت شما : {verify_code} می باشد",
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    background_task.add_task(fm.send_message, message)
