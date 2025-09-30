from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import jwt
from app import crud

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 配置
SECRET_KEY = "mysecretkey"  # 生产环境请用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_data: dict):
        existing_user = await crud.get_user_by_username(self.db, user_data["username"])
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        user = await crud.create_user(self.db, user_data)
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

    async def login(self, username: str, password: str):
        user = await crud.get_user_by_username(self.db, username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
