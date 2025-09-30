from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin, TokenOut
from app.services.auth import AuthService
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=TokenOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register(user.model_dump())

@router.post("/login", response_model=TokenOut)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(data.username, data.password)
