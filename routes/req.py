
from fastapi import (
    APIRouter,
    Request,
   
)


#router settings / routing rules
router = APIRouter(
    prefix="/req",
    tags=["req"],
    responses={
        404: {"description": "Not found Here"}
    })

@router.get("/all")
def allrequests(request: Request):

    #set session values
    request.session["visited"] = True
    request.session["name"] = "Victor Okenyi"
    request.session["club"] = "Manchester United"
    request.state.user = "Developer"
    
    #delete session value
    # del request.session["name"]
    request.session.pop("name", None) #delete session value safely
    
    return {
        "method": request.method,
        "url": request.url.path,
        "headers": dict(request.headers),
        "agent": request.headers.get("user-agent"),
        "ip": request.client.host,
        "client": request.client,
        "user": request.headers.get("user"),
        "cookies": request.cookies,
        "referer": request.headers.get("referer"),
        "session": request.session,
        "myname": request.session.get("name"), #get session value
        "myclub": request.session.get("club"), #get session value
        # "scope": request.scope,
        "state": request.state,
        "query_params": dict(request.query_params)
    }
