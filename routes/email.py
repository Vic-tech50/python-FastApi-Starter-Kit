from fastapi import (
    APIRouter,
    Request,
    Form,
    BackgroundTasks
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# import time
# import models
from database import SessionLocal
from services.mail import send_email
from passlib.context import CryptContext # PASSWORD HASHER(pip install passlib[bcrypt])





#router settings / routing rules
router = APIRouter(
    prefix="/email",
    tags=["email"],
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




@router.get("/")
def index(request: Request):
    success = request.session.pop("success", None) #to display success message after email is sent and then remove it from session to prevent it from showing again on page refresh
    return templates.TemplateResponse(request, "email/index.html", {"success": success})





@router.post("/sendemail")
def send_contact_email(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    comment: str = Form(...),
):

# SEND EMAIL IN BACKGROUND
    background_tasks.add_task(
        send_email,
        recipient="email@example.com",
        subject=f"New Contact Message From {name}",
        template_name="emails/message.html",
        context={
        "name": name,
        "comment": comment,
        "email": email
         }
        # body=f"""
        # <h3>New Contact Message</h3>

        # <p><strong>Name:</strong> {name}</p>

        # <p><strong>Email:</strong> {email}</p>

        # <p><strong>Comment:</strong></p>

        # <p>{comment}</p>
        # """
    )

    request.session["success"] = "Email sent successfully!"

    return RedirectResponse(
        url=request.headers.get("referer", "/"),
        status_code=303
    )