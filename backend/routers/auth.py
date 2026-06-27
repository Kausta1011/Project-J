from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter()

class User(BaseModel):
    username : str
    password : str

@router.post("/register")
async def register(user : User):
    #hash password.     ← needs passlib (not learned yet)
    #save to DB.        ← needs SQLModel + PostgreSQL (not learned yet)
    return {"message" : "User Created"}

@router.post("/login")
async def login():
    #verify credintials.     ← needs DB query + hash comparison (not learned yet
    #issue JWT token         ← needs python-jose (not learned yet)

    return {"access token" : token}

    


