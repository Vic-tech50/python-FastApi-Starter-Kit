from fastapi import FastAPI, Form, Request, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import uuid

load_dotenv()

router = APIRouter(
    prefix="/paystack",
    tags=["paystack"],
    responses={
        404: {"description": "Not found Here"}
    })

templates = Jinja2Templates(directory="templates")

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")


# Payment Form
@router.get("/")
def payment_page(request: Request):

    return templates.TemplateResponse(request,"payment.html")


# Initialize Payment
@router.post("/pay")
def pay(
    email: str = Form(...),
    amount: float = Form(...)
):

    reference = str(uuid.uuid4())

    url = "https://api.paystack.co/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "routerlication/json"
    }

    payload = {
        "email": email,
        "amount": int(amount * 100),  # Kobo
        "reference": reference,
        "callback_url": "http://127.0.0.1:8000/paystack/callback"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    result = response.json()

    if not result.get("status"):
        raise HTTPException(
            status_code=400,
            detail=result.get("message")
        )

    payment_url = result["data"]["authorization_url"]

    return RedirectResponse(
        url=payment_url,
        status_code=303
    )


# Callback after payment
@router.get("/callback")
def callback(reference: str):

    url = (
        f"https://api.paystack.co/"
        f"transaction/verify/{reference}"
    )

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(
        url,
        headers=headers
    )

    result = response.json()

    if (
        result["status"]
        and result["data"]["status"] == "success"
    ):

        #send to database
        # payment = models.Payment(
        # email=email,
        # amount=amount,
        # reference=reference,
        # status="paid"
        # )

        # db.add(payment)
        # db.commit()
        
        #return Html
    #       return templates.TemplateResponse(
    #     "success.html",
    #     {
    #         "request": request,
    #         "reference": reference,
    #         "amount": amount,
    #         "email": email
    #     }
    # )

        return {
            "message": "Payment Successful",
            "email": result["data"]["customer"]["email"],
            "amount": result["data"]["amount"] / 100,
            "reference": reference
        }

    return {
        "message": "Payment Failed"
    }