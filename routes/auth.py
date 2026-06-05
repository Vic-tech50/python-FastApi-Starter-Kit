from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request, Form, BackgroundTasks
from fastapi.responses import RedirectResponse
from services.mail2 import send_email
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from fastapi.templating import Jinja2Templates
import models
from passlib.context import CryptContext # PASSWORD HASHER(pip install passlib[bcrypt])

templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# router = APIRouter()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"description": "Not found Here"}
    }
)


# DATABASE CONNECTION
def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(request, "login.html", {
        "error": request.session.pop("error", None),
        "success": request.session.pop("success", None)
    })


# LOGIN LOGIC
@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # 1. FIND USER
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 2. VERIFY PASSWORD
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 3. REDIRECT TO DASHBOARD
    return RedirectResponse(url="/home/dashboard", status_code=303)

@router.get("/forgot-password")
def forgot_password_page(request: Request):

    success = request.session.pop(
        "success",
        None
    )

    error = request.session.pop(
        "error",
        None
    )

    return templates.TemplateResponse(
       request, "forgot-password.html",
        {
           
            "success": success,
            "error": error
        }
    )
    

@router.post("/forgot-password")
def send_reset_link(
    request: Request,
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    db: Session = Depends(get_db)
):

    # CHECK IF USER EXISTS
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if not user:

        request.session["error"] = "Email not found"

        return RedirectResponse(
            "/auth/forgot-password",
            status_code=303
        )

    try:

        reset_link = (
            f"http://localhost:8000/auth/reset-password"
            f"?email={user.email}"
        )

        # SEND EMAIL IN BACKGROUND
        background_tasks.add_task(
            send_email,
            recipient=user.email,
            subject="Password Reset Request",
            body=f"""
            <h1>Hello {user.name}</h1>

            <p>
                We received a request to reset your password.
            </p>

            <p>
                Click the button below:
            </p>

            <a href="{reset_link}">
                Reset Password
            </a>
            """
        
          )

        request.session["success"] = (
            "Password reset link has been sent."
        )

    except Exception as e:

        print("Email Error:", e)

        request.session["error"] = (
            "Failed to send email."
        )

    return RedirectResponse(
        "/auth/forgot-password",
        status_code=303
    )

@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse(request, "register.html")


@router.post("/register")
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

      # CHECK IF EMAIL EXISTS
    existing_user = db.query(models.User)\
        .filter(models.User.email == email)\
        .first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    
     # PASSWORD VALIDATION
    if len(password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must not exceed 72 characters"
        )

    # HASH PASSWORD
    hashed_password = pwd_context.hash(password)
    status = "active"

    # CREATE USER
    user = models.User(
        name=name,
        email=email,
        status=status,
        password=hashed_password
    )

    db.add(user)
    db.commit()

    try:
        send_email(
            recipient=email,
            subject="Welcome to Our Platform",
            body=f"""
            <h1>Hello {name}</h1>

            <p>
                Welcome to our platform.
            </p>

            <p>
                Your account has been created successfully.
            </p>
            """
        )

    except Exception as e:
        print("Email Error:", e)


      # REDIRECT TO LOGIN
    return RedirectResponse(
        url="/auth/login",
        status_code=303,
        headers={"message": "User created"}
    )
