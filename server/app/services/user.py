from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user as crud
from app.schemas.user import UserCreate

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate):
        existing_user = await crud.get_user_by_email(self.db, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return await crud.create_user(self.db, user)

    async def get_user(self, user_id: int):
        user = await crud.get_user(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def list_users(self, skip: int = 0, limit: int = 10):
        return await crud.get_users(self.db, skip=skip, limit=limit)
