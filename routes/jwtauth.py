from fastapi import APIRouter, Form, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta
import models
from database import SessionLocal
from auth.jwt import create_access_token
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse



limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/jwt",
    tags=["jwt"],
    responses={
        404: {"description": "Not found Here"}
    })

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if not user:
        request.session["error"] = "Invalid credentials"

        return RedirectResponse(
            url=request.headers.get("referer", "/"),
            status_code=303
        )

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():

        remaining = int(
            (user.locked_until - datetime.utcnow()).total_seconds()
        )

        request.session["error"] = (
            f"Account locked. Try again in {remaining} seconds."
        )

        return RedirectResponse(
            url=request.headers.get("referer", "/"),
            status_code=303
        )

    # Wrong password
    if not pwd_context.verify(password, user.password):

        user.failed_attempts += 1

        if user.failed_attempts == 1:

            db.commit()

            request.session["error"] = (
                "Wrong password. 2 attempts remaining."
            )

            return RedirectResponse(
                url=request.headers.get("referer", "/"),
                status_code=303
            )

        elif user.failed_attempts == 2:

            db.commit()

            request.session["error"] = (
                "Wrong password. 1 attempt remaining."
            )

            return RedirectResponse(
                url=request.headers.get("referer", "/"),
                status_code=303
            )

        elif user.failed_attempts >= 3:

            user.locked_until = (
                datetime.utcnow() + timedelta(minutes=5)
            )

            user.failed_attempts = 0

            db.commit()

            request.session["error"] = (
                "Too many failed attempts. Account locked for 5 minutes."
            )

            return RedirectResponse(
                url=request.headers.get("referer", "/"),
                status_code=303
            )

    # Successful login
    user.failed_attempts = 0
    user.locked_until = None

    db.commit()

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    response = RedirectResponse(
        url="/home/dashboard",
        status_code=303
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    request.session["success"] = (
        f"Welcome back, {user.name}"
    )

    return response



# RATE LIMIT EXAMPLE api
@router.post("/loginapi")
# @limiter.limit("5/seconds")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    #check if user exists
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():

        remaining = int(
            (user.locked_until - datetime.utcnow()).total_seconds()
        )
        request.session["error"] = f"Account locked. Try again in {remaining} seconds."
        return RedirectResponse(
        url=request.headers.get("referer", "/"),
        status_code=303
        )

       

            # raise HTTPException(
            #     status_code=403,
            #     detail=f"Account locked. Try again in {remaining} seconds."
            # )

    # Verify password
    if not pwd_context.verify(password, user.password):

        user.failed_attempts += 1

        # Warning messages
        if user.failed_attempts == 1:
            warning = "Wrong password. 2 attempts remaining."

        elif user.failed_attempts == 2:
            warning = "Wrong password. 1 attempt remaining."

        elif user.failed_attempts >= 3:

            user.locked_until = datetime.utcnow() + timedelta(minutes=5)
            user.failed_attempts = 0

        if db.commit():
            request.session["error"] = "Too many failed attempts. Account locked for 5 minutes."
            return RedirectResponse(
            url=request.headers.get("referer", "/"),
            status_code=303
            )

       

            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail="Too many failed attempts. Account locked for 5 minutes."
            # )

        db.commit()



        request.session["error"] = warning

        return RedirectResponse(
        url=request.headers.get("referer", "/"),
        status_code=303
    )

        # raise HTTPException(
        #     status_code=400,
        #     detail=warning
        # )

    # Successful login
    user.failed_attempts = 0
    user.locked_until = None

    db.commit()

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    response = RedirectResponse(
        url="/home/dashboard",
        status_code=303
    )

    # Optional: save token in cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )

    return response

# Simple JWT LOGIN
@router.post("/loginjwt")
# @limiter.limit("5/seconds")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    return RedirectResponse(url="/home/dashboard", status_code=303)

    # return {
    #     "access_token": token,
    #     "token_type": "bearer",
    #     "message": "Login successful"

    # }

@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/auth/login",
        status_code=303
    )

    response.delete_cookie("access_token")

    return response