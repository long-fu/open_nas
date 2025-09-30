from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, TokenOut
from app.services.user import UserService
from app.database import get_db

router = APIRouter()

@router.post("/users/", response_model=TokenOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.create_user(user)

@router.get("/users/{user_id}", response_model=TokenOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_user(user_id)

@router.get("/users/", response_model=list[TokenOut])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.list_users(skip=skip, limit=limit)
