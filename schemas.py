from pydantic import BaseModel
from typing import Optional

# CREATE
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    created_at: str

# RESPONSE
class User(UserCreate):
    id: int

    class Config:
        orm_mode = True

# CREATE
class BlogCreate(BaseModel): 
    title: str
    description: str
    created_at: str
    updated_at: str
    

# RESPONSE
class Blog(BlogCreate):
    id: int

    class Config:
        orm_mode = True
        