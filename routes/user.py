from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from dependencies.auth import admin_required, user_required

from auth.jwt import verify_token

security = HTTPBearer()


# Protect the Entire Router
# router = APIRouter(
#     prefix="/admin",
#     tags=["Admin"],
#     dependencies=[
#         Depends(admin_required)
#     ]
# )

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        404: {"description": "Not found Here"}
    }
)

# html templating
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
def dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "message": "Welcome to dashboard",
        "user": payload
    }
    
@router.get("/admindashboard")
def index(request: Request, auth=Depends(admin_required)):
    # admin_required(request)
  #  success = request.session.pop("success", None) #to display success message after email is sent and then remove it from session to prevent it from showing again on page refresh
    return templates.TemplateResponse(request, "home/admindashboard.html")


@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "home/dashboard.html")


