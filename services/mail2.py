import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))


def send_email(
    recipient: str,
    subject: str,
    body: str
):

    try:

        msg = MIMEMultipart()

        msg["From"] = MAIL_USERNAME
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(
            MIMEText(body, "html")
        )

        server = smtplib.SMTP(
            MAIL_SERVER,
            MAIL_PORT
        )

        server.starttls()

        server.login(
            MAIL_USERNAME,
            MAIL_PASSWORD
        )

        server.sendmail(
            MAIL_USERNAME,
            recipient,
            msg.as_string()
        )

        server.quit()

        return True

    except Exception as e:
        print(e)
        return False