from fastapi import APIRouter, FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
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
    prefix="/home",
    tags=["home"],
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


@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "home/dashboard.html")

