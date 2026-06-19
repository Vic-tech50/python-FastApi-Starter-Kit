
from fastapi import APIRouter,Request,Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from services.mail2 import send_email
import random
import models
import secrets
from database import SessionLocal
from datetime import datetime
from datetime import timedelta
from passlib.context import CryptContext # PASSWORD HASHER(pip install passlib[bcrypt])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)





#router settings / routing rules
router = APIRouter(
    prefix="/otp",
    tags=["otp"],
    responses={
        404: {"description": "Not found Here"}
    })

# html templating
templates = Jinja2Templates(directory="templates")

#database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# def generate_otp():

#     return str(random.randint(100000,99999))

@router.get("/")
def otp(request: Request):
    return templates.TemplateResponse(request,"otp.html")

@router.get("/verify-otp")
def otp(request: Request):
    success = request.session.pop("success", None) 
    error = request.session.pop("error", None) 
    return templates.TemplateResponse(request,"verify-otp.html",
                                      {
                                          "success": success,
                                          "error": error,
                                       }
                                      )


@router.post("/send-otp")
def send_otp(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):

    # Generate secure OTP
    # otp = str(
    #     secrets.randbelow(900000) + 100000
    # )
    # otp = random.randint(100000,999999)
    otp = str(secrets.randbelow(900000) + 100000)
    hashed_otp = pwd_context.hash(otp)

    # Expiry time
    expires_at = (datetime.utcnow()+ timedelta(minutes=5))

    # Remove previous OTP for this email
    db.query(models.OTP)\
        .filter(models.OTP.email == email)\
        .delete()

    # Create new OTP record
    otp_record = models.OTP(
        email=email,
        otp=hashed_otp,
        expires_at=expires_at
    )

    db.add(otp_record)
    db.commit()

    # Store email only
    request.session["email"] = email

    # Send email
    send_email(
        recipient=email,
        subject="OTP Verification",
        body=f"""
        <h2>Your OTP Code</h2>

        <h1>{otp}</h1>

        <p>
            This code expires in 5 minutes.
        </p>
        """
    )

    request.session["success"] = ("OTP sent successfully")

    return RedirectResponse("/otp/verify-otp",status_code=303)


# @router.post("/send-otp")
# def send_otp(
#     request: Request,
#     email: str = Form(...)
# ):

#     otp = random.randint(100000,999999)

#     request.session["otp"] = otp
#     request.session["email"] = email
    
#     request.session["otp_expiry"] = (datetime.utcnow()+ timedelta(minutes=5)).isoformat()

#     # print("OTP:", otp)
#     # Send Email Here
#     send_email(
#     recipient=email,
#     subject="OTP Verification",
#     body=f"""
#     <h2>Your OTP</h2>

#     <h1>{otp}</h1>

#     <p>
#         This code expires in 5 minutes.
#     </p>
#     """
# )
#     return RedirectResponse("/otp/verify-otp",status_code=303)


@router.post("/verify-otp")
def verify_otp(
    request: Request,
    otp: str = Form(...),
    db: Session = Depends(get_db)
):

    email = request.session.get("email")

    if not email:
        request.session["error"] = ("Session expired. Request a new OTP.")
        return RedirectResponse( url=request.headers.get("referer", "/"),status_code=303)

    # Find OTP record
    otp_record = (db.query(models.OTP).filter(models.OTP.email == email).first())

    if not otp_record:
        request.session["error"] = ("OTP not found.")
        return RedirectResponse( url=request.headers.get("referer", "/"),status_code=303)

    # Check expiry
    if datetime.utcnow() > otp_record.expires_at:

        db.delete(otp_record)
        db.commit()

        request.session["error"] = ("OTP has expired.")
        return RedirectResponse( url=request.headers.get("referer", "/"),status_code=303)

    # Verify OTP
    # if otp != otp_record.otp:
    if not pwd_context.verify(otp, otp_record.otp):
        request.session["error"] = ("Invalid OTP.")
        return RedirectResponse( url=request.headers.get("referer", "/"),status_code=303)

    # OTP VERIFIED
    db.delete(otp_record)
    db.commit()

    request.session["otp_verified"] = True
    request.session["success"] = (
        "OTP Verified Successfully"
    )
    return RedirectResponse( url=request.headers.get("referer", "/"),status_code=303)

# @router.post("/verify-otp")
# def verify_otp(request: Request, otp: str = Form(...)):
#     #get otp saved in the session
#     saved_otp = request.session.get("otp")

#     if otp != saved_otp:

#         request.session["error"] = ("Invalid OTP")

#         return RedirectResponse( url=request.headers.get("referer", "/"),status_code=303)
    
#     expiry = datetime.fromisoformat(request.session["otp_expiry"])
#     if datetime.utcnow() > expiry:

#         request.session["error"] = (
#         "OTP Expired"
#     )
#     request.session["success"] = ("OTP Verified")
#     return {
#         "message":"Payment successful"
#         }

    # return RedirectResponse("/reset-password",status_code=303)
    
