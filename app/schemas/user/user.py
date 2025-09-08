from pydantic import BaseModel, EmailStr
from typing import Optional

#Entrada de datos, cuando el cliente manda los datos


class UserCreate(BaseModel):
    first_name_one: str
    first_name_two: Optional[str] = None
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


class UserInfoName (BaseModel):
    email : EmailStr   


class DeleteUserForEmail(BaseModel):
    email : EmailStr   

class UpdateUserPut(BaseModel):
    first_name_one: str
    first_name_two: Optional[str] = None
    last_name_one: str
    last_name_two: str
    email: EmailStr



class UpdateUserPutOut(BaseModel):
    first_name_one: str
    first_name_two: Optional[str] = None
    last_name_one: str
    last_name_two: str
    email: EmailStr
