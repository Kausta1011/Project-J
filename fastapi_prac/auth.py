# auth.py ties all your previous files together into one route. It needs to:

# Accept the incoming request (UserCreate -- email + password)
# Hash the password (hash_password from hashing.py)
# Create a User object with the hashed password
# Save it to the DB via session (add → commit → refresh)
# Return the new user's id and email
# In terms of imports, you'll need:

# APIRouter from fastapi
# Session, Depends from fastapi/sqlmodel
# UserCreate, User from models/user.py
# hash_password from auth/hashing.py
# get_session from database.py


from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select

from user import UserCreate, User
from hashing import hash_password
from database import get_session

router = APIRouter()

@router.post("/register")
def resigter(user :  UserCreate, session: Session = Depends(get_session)):

    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    password = hash_password(user.password)
    candidate = User(email=user.email, hashed_password=password)
    session.add(candidate)
    session.commit()
    session.refresh(candidate)
    return {"id":candidate.id, "email" : candidate.email}

