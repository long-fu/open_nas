from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import jwt
from app.crud import user as crud
from app.schemas.user import TokenOut
# JWT 配置
SECRET_KEY = "mysecretkey"  # 生产环境请用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(
    schemes=["argon2", "pbkdf2_sha256"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_data: dict) -> TokenOut: 
        existing_user = await crud.get_user_by_username(self.db, user_data["username"])
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        user = await crud.create_user(self.db, user_data)
        token = create_access_token({"sub": user.username})
        return TokenOut(access_token=token, token_type='bearer')

    async def login(self, username: str, password: str) -> TokenOut:
        user = await crud.get_user_by_username(self.db, username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": user.username})
        return TokenOut(access_token=token, token_type='bearer')
