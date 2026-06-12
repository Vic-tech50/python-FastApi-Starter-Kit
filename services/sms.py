from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)


def send_sms(
    to: str,
    message: str
):

    sms = client.messages.create(
        body=message,
        from_=PHONE_NUMBER,
        to=to
    )

    return sms.sid