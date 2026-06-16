from fastapi import Request
from fastapi import HTTPException

def admin_required(
    request: Request
):

    if (
        "id" not in request.session
    ):

        raise HTTPException(
            status_code=401,
            detail="Login required"
        )

    if (
        request.session["role"]
        != "admin"
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )
        
def user_required(request: Request):
    print(request.session)
    if ("id" not in request.session):
        raise HTTPException(status_code=401,detail="Login required")

    if(request.session["role"] != "user"):
        # request.session.get("role")
        # != "user"
         raise HTTPException(status_code=403,detail="Access denied")