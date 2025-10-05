from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserInfo
from app.services.user import UserService
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user, api_key_header
# from fastapi.security.api_key import APIKeyHeader
from fastapi import Security
# from app.services.auth import AuthService, verify_access_token
# from app.routers.user import get_current_user
# api_key_header = APIKeyHeader(name="Authorization")

router = APIRouter()

@router.get("/users/info", response_model=UserInfo)
async def read_user(db: AsyncSession = Depends(get_db), api_key: str = Security(api_key_header)):
    username = get_current_user(api_key)
    service = UserService(db)
    # FIXME: 这里直接把 User -> 转换成 UserInfo
    return await service.get_user(username)

# @router.get("/users/", response_model=list[UserInfo])
# async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
#     service = UserService(db)
#     return await service.list_users(skip=skip, limit=limit)
