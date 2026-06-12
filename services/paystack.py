import requests
import os
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET = os.getenv(
    "PAYSTACK_SECRET_KEY"
)

def initialize_payment(
    email: str,
    amount: int
):

    url = (
        "https://api.paystack.co/"
        "transaction/initialize"
    )

    headers = {
        "Authorization":
        f"Bearer {PAYSTACK_SECRET}"
    }

    payload = {
        "email": email,
        "amount": amount * 100
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    return response.json()


def verify_payment(
    reference: str
):

    url = (
        f"https://api.paystack.co/"
        f"transaction/verify/{reference}"
    )

    headers = {
        "Authorization":
        f"Bearer {PAYSTACK_SECRET}"
    }

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()