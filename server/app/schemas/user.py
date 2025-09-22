from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    uid: str
    name: str
    email: EmailStr
    phone: str
    password: str
    gender: str = "未知"
    age: int = 18
    status: str = "正常"
    
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
