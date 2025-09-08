from pydantic import BaseModel, EmailStr

class LoginUserData(BaseModel):
    email: EmailStr
    password: str

class LoginUserOut(BaseModel):
    fullname: str
    email: EmailStr
    acces_token: str
    token_type: str

