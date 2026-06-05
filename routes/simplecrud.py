# routes/users.py


import email

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import SessionLocal

router = APIRouter(
    prefix="/crud",
    tags=["crud"],
    responses={
        404: {"description": "Not found Here"}
    })

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.get("/blog/create")
def login(request: Request):
    # flash = request.session.pop("flash", None)
    return templates.TemplateResponse(request, "crud/create.html")
    

@router.post("/store")
def create_blog(
    request: Request,
    title: str = Form(...),
    comment: str = Form(...),
    db: Session = Depends(get_db)
):
   

    blog = models.Blog(
        title=title,
        description=comment
    )

    db.add(blog)
    db.commit()

    # request.session["flash"] = "Blog created successfully!"

    return RedirectResponse(
         url=request.headers.get("referer", "/"),
        # "/crud/blog/create",
        status_code=303
    )

@router.get("/blog")
def blogs(
    request: Request,
    db: Session = Depends(get_db)
):

    blogs = db.query(models.Blog).all()
    print(blogs)  # Debug

    return templates.TemplateResponse(
       request,"crud/index.html", { "blogs": blogs}
    #    {"blogs": blogs}
    )

@router.get("/blog/edit/{blog_id}")
def edit_blog(
    request: Request,
    blog_id: int,
    db: Session = Depends(get_db)
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    return templates.TemplateResponse(request, "crud/edit.html", {"blog": blog})

@router.post("/blog/update/{id}")
def update_user(
    id: int,
    title: str = Form(...),
    comment: str = Form(...),
    db: Session = Depends(get_db)
):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if blog:
        blog.title = title
        blog.description = comment

    db.commit()
    db.refresh(blog)


    return RedirectResponse(
        "/crud/blog",
        status_code=303
    )

@router.post("/blog/delete/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db)
):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if blog:
        db.delete(blog)
        db.commit()


    return RedirectResponse(
        "/crud/blog",
        status_code=303
    )
