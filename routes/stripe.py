from fastapi import FastAPI, Form, Request, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import stripe
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

router = APIRouter(
    prefix="/stripe",
    tags=["stripe"],
    responses={
        404: {"description": "Not found Here"}
    })

templates = Jinja2Templates(directory="templates")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# -----------------------
# HOME PAGE
# -----------------------
@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request,"stripepayment.html")


# -----------------------
# CREATE STRIPE SESSION
# -----------------------
@router.post("/pay")
def pay(
    email: str = Form(...),
    amount: float = Form(...)
):

    session = stripe.checkout.Session.create(
        payment_method_types=["card", "us_bank_account", "link"],
        customer_email=email,
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "FastAPI Product Payment",
                    },
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/cancel",
    )

    return RedirectResponse(
        url=session.url,
        status_code=303
    )


# -----------------------
# SUCCESS PAGE
# -----------------------
@router.get("/success")
def success(session_id: str):

    session = stripe.checkout.Session.retrieve(session_id)

    return {
        "message": "Payment Successful",
        "email": session.customer_details.email,
        "amount": session.amount_total / 100,
        "currency": session.currency
    }


# -----------------------
# CANCEL PAGE
# -----------------------
@router.get("/cancel")
def cancel():
    return {
        "message": "Payment cancelled"
    }