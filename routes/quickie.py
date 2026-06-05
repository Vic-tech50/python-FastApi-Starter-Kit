import os
import shutil
from uuid import uuid4

from fastapi import (
    APIRouter,
    Request,
    Form,
    File,
    UploadFile,
    Depends
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal





#router settings / routing rules
router = APIRouter(
    prefix="/crudimage",
    tags=["crudimage"],
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

