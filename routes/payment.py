from fastapi import (
    APIRouter,
    Depends
)
from services.paystack import initialize_payment, verify_payment
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter(
    prefix="/pay",
    tags=["pay"],
    responses={
        404: {"description": "Not found Here"}
    })

#database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/paystack/pay")
def pay(
    email: str,
    amount: int
):

    payment = initialize_payment(
        email,
        amount
    )

    return payment

@router.get("/paystack/verify/{reference}")
def verify(
    reference: str,
    db: Session = Depends(get_db)
):

    result = verify_payment(
        reference
    )

    if (
        result["data"]["status"]
        == "success"
    ):

        payment = Payment(
            email=result["data"]["customer"]["email"],
            amount=result["data"]["amount"] / 100,
            reference=reference,
            provider="paystack",
            status="paid"
        )

        db.add(payment)
        db.commit()

        return {
            "message":
            "Payment successful"
        }

    return {
        "message":
        "Payment failed"
    }