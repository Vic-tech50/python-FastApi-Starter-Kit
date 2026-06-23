from fastapi import APIRouter
import httpx

router = APIRouter(
    prefix="/client",
    tags=["client"],
    responses={
        404: {"description": "Not found Here"}
    })

@router.get("/")
async def get_users():

    async with httpx.AsyncClient() as client:

        response = await client.get(
            "https://jsonplaceholder.typicode.com/users/"
        )

    return response.json()

@router.get("/client/{id}")
async def get_user(id: int):

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"https://jsonplaceholder.typicode.com/users/{id}"
        )

    return response.json()