from pydantic import BaseModel, EmailStr
from typing import Optional

#Entrada de datos, cuando el cliente manda los datos


class UserCreate(BaseModel):
    fist_name_one: str
    fist_name_two: Optional[str] = None
    last_name_one: str
    last_name_two: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

class UserInfo(BaseModel):
    id: int
    email: EmailStr
    fullname: str