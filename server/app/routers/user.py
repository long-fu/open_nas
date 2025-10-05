from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserInfo
from app.services.user import UserService
from app.database import get_db
from app.models.user import User
router = APIRouter()

@router.get("/users/{user_name}", response_model=UserInfo)
async def read_user(username: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.get_user(username)

# @router.get("/users/", response_model=list[UserInfo])
# async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
#     service = UserService(db)
#     return await service.list_users(skip=skip, limit=limit)
