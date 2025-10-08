from pydantic import BaseModel, EmailStr
from datetime import date
class UserLogin(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    uid: str | None = None
    username: str
    email: EmailStr
    phone: str
    password: str
    gender: str = "未知"
    birthdate: date | None = None
    status: str = "正常"
    class Config:
        orm_mode = True
        
class UserInfo(BaseModel):
    uid: str | None = None
    username: str
    email: EmailStr
    phone: str
    gender: str = "未知"
    birthdate: date | None = None
    status: str = "正常"


