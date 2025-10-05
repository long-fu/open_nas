from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin, TokenOut
from app.services.auth import AuthService, verify_access_token
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.api_key import APIKeyHeader

router = APIRouter()

# router = APIRouter(prefix="/auth", tags=["Auth"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

api_key_header = APIKeyHeader(name="Authorization")


@router.post("/register", response_model=TokenOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register(user.model_dump())

@router.post("/auth/login", response_model=TokenOut)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    print(data.username, data.password)
    service = AuthService(db)
    return await service.login(data.username, data.password)

# 验证 Token 依赖
def get_current_user(token: str):
    
    payload = verify_access_token(token)
    print(payload)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["sub"]  # 返回 username

