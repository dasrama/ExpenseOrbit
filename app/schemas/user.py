
from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: int
    email: EmailStr
       

class UserLogin(BaseModel):
    email: EmailStr
    password: str