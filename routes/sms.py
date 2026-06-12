from fastapi import APIRouter, BackgroundTasks, Depends
from services.sms import send_sms
from fastapi.security import OAuth2PasswordBearer

#router settings / routing rules
router = APIRouter(
    prefix="/sms",
    tags=["sms"],
    responses={
        404: {"description": "Not found Here"}
    })

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/testsms")
def test_sms(
    background_tasks: BackgroundTasks,
    token: str = Depends(oauth2_scheme)
):

    # sid =  send_sms(
    #     "+2347088366968",
    #     "Hello from FastAPI"
    # )
    
    background_tasks.add_task(
        send_sms, 
        "+2347088366968",
        "Hello from FastAPI written by victech"
        
    )
        

    return {
        "message": "Message Sent",
        "token": token
        
    }