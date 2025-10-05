from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.crud import user as crud
from app.schemas.user import TokenOut
from jose import JWTError, jwt

# JWT 配置
SECRET_KEY = "mysecretkey"  # 生产环境请用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# 创建密码加密上下文
pwd_context = CryptContext(
    schemes=["argon2", "pbkdf2_sha256"],
    deprecated="auto"
)

# 加密密码
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

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
