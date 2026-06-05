from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.jwt import verify_token

security = HTTPBearer()

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        404: {"description": "Not found Here"}
    }
)

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