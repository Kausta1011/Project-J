from sqlmodel import SQLModel, Field

class UserCreate(SQLModel):
    email : str
    password : str

class User(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key=True)
    email : str
    hashed_password : str