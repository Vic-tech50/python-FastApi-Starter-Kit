import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT"))

# Load templates
env = Environment(
    loader=FileSystemLoader("templates")
)


def render_template(
    template_name: str,
    context: dict = {}
):

    template = env.get_template(template_name)

    return template.render(**context)


def send_email(
    recipient: str,
    subject: str,
    template_name: str,
    context: dict = {}
):

    try:

        html_body = render_template(
            template_name,
            context
        )

        msg = MIMEMultipart()

        msg["From"] = MAIL_USERNAME
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(
            MIMEText(html_body, "html")
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

        print("Email Error:", e)

        return False