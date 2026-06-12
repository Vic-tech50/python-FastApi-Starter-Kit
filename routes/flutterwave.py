from fastapi import FastAPI, Form, Request, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import uuid

load_dotenv()

router = APIRouter(
    prefix="/flutter",
    tags=["flutter"],
    responses={
        404: {"description": "Not found Here"}
    })


templates = Jinja2Templates(directory="templates")

FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY")


# =========================
# PAYMENT PAGE
# =========================

@router.get("/")
def payment_page(request: Request):

    return templates.TemplateResponse(
        request,
        "flutterpayment.html"
    )


# =========================
# INITIALIZE PAYMENT
# =========================

@router.post("/pay")
def pay(
    email: str = Form(...),
    amount: float = Form(...)
):

    tx_ref = str(uuid.uuid4())

    url = "https://api.flutterwave.com/v3/payments"

    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "routerlication/json"
    }

    payload = {
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": "NGN",
        "redirect_url": "http://127.0.0.1:8000/flutter/callback",
        "customer": {
            "email": email,
            "name": "Victor",
            # "phonenumber": "08012345678"
        },
        # "customizations": {
        #     "title": "My FastAPI Store",
        #     "description": "Payment for services"
        # }
    }

   
    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    result = response.json()
    print(result)

    if result.get("status") != "success":

        raise HTTPException(
            status_code=400,
            detail=result.get("message")
        )

    payment_link = result["data"]["link"]

    return RedirectResponse(
        url=payment_link,
        status_code=303
    )


# =========================
# CALLBACK
# =========================

@router.get("/callback")
def callback(
    request: Request,
    transaction_id: str = None,
    tx_ref: str = None
):

    if not transaction_id:

        raise HTTPException(
            status_code=400,
            detail="Transaction ID missing"
        )

    verify_url = (
        f"https://api.flutterwave.com/v3/"
        f"transactions/{transaction_id}/verify"
    )

    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"
    }

    response = requests.get(
        verify_url,
        headers=headers
    )

    result = response.json()

    if (
        result.get("status") == "success"
        and result["data"]["status"] == "successful"
    ):

        email = result["data"]["customer"]["email"]
        amount = result["data"]["amount"]

        return templates.TemplateResponse(
            request,
            "success.html",
            {
                "email": email,
                "amount": amount,
                "reference": tx_ref
            }
        )

    return {
        "message": "Payment Failed"
    }