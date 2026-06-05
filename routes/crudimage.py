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



# CREATE crud image
@router.get("/create")
def create(
    request: Request
):

    errors = request.session.pop("errors", {})
    old = request.session.pop("old", {})
    success = request.session.pop("success", None)

    return templates.TemplateResponse(request,
        "crudimage/create.html",
          {
            "errors": errors,
            "old": old,
            "success": success
        }
    )
# @router.get("/create")
# def create(request: Request):
#     # flash = request.session.pop("flash", None)
#     return templates.TemplateResponse(request, "crudimage/create.html")
    
# CREATE crud image LOGIC
@router.post("/store")
async def save(
    request: Request,
    name: str = Form(...),
    age: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Store old values
    request.session["old"] = {
        "name": name,
        "age": age
    }

    errors = {}

    # Name validation
    if not name.strip():
        errors["name"] = "Name field is required"

    elif len(name) < 3:
        errors["name"] = "Name must be at least 3 characters"

    elif name.isdigit():
        errors["name"] = "Name cannot be numbers only"

    # Age validation
    if not age.strip():
        errors["age"] = "Age field is required"

    elif not age.isdigit():
        errors["age"] = "Age must be a number"

    # Image validation
    if not image.filename:
        errors["image"] = "Image is required"

    if errors:
        request.session["errors"] = errors

        return RedirectResponse(
            url="/crudimage/create",
            status_code=303
        )

    try:

        extension = image.filename.split(".")[-1]

        filename = f"{uuid4()}.{extension}"

        filepath = f"uploads/blogs/{filename}"

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                image.file,
                buffer
            )

        student = models.Student(
            name=name,
            age=age,
            passport=filename
        )

        db.add(student)
        db.commit()

        request.session["success"] = "Student created successfully"

        return RedirectResponse(
            url="/crudimage/create",
            status_code=303
        )

    except Exception as e:

        request.session["errors"] = {
            "general": str(e)
        }

        return RedirectResponse(
            url="/crudimage/create",
            status_code=303
        )

@router.get("/index")
def index(
    request: Request,
    db: Session = Depends(get_db)
):

    crudimages = db.query(models.Student).all()
    print(crudimages)  # Debug

    return templates.TemplateResponse(
       request,"crudimage/index.html", { "crudimages": crudimages}
    #    {"crudimages": crudimages}
    )

@router.get("/edit/{id}")
def edit(
    request: Request,
    id: int,
    db: Session = Depends(get_db)
):
    crudimage = db.query(models.Student).filter(models.Student.id == id).first()
    return templates.TemplateResponse(request, "crudimage/edit.html", {"crudimage": crudimage})

@router.post("/update/{id}")
def update_user(
    id: int,
    name: str = Form(...),
    age: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)  
):
    
    if image.filename:
        extension = image.filename.split(".")[-1]
        filename = f"{uuid4()}.{extension}"
        filepath = f"uploads/blogs/{filename}"

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                image.file,
                buffer
            )
    


    crudimage = db.query(models.Student).filter(models.Student.id == id).first()
    
    if crudimage:
        crudimage.name = name
        crudimage.age = age
        if image.filename: 
          crudimage.passport = filename

    db.commit()
    db.refresh(crudimage)


    return RedirectResponse(
        "/crudimage/index",
        status_code=303
    )

@router.post("/delete/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db)
):

    crudimage = db.query(models.Student).filter(models.Student.id == id).first()

    if crudimage:
        db.delete(crudimage)
        db.commit()


    return RedirectResponse(
        "/crudimage/index",
        status_code=303
    )
