from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user as crud

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # async def create_user(self, user: UserCreate):
    #     existing_user = await crud.get_user_by_email(self.db, user.email)
    #     if existing_user:
    #         raise HTTPException(status_code=400, detail="Email already registered")
    #     return await crud.create_user(self.db, user)

    async def get_user(self, uid: str):
        user = await crud.get_user_by_uid(self.db, uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # info = UserInfo(
        #     uid=user.uid,
        #     username=user.username,
        #     email=user.email,
        #     phone=user.phone,
        #     gender=user.gender,
        #     birthdate=user.birthdate,
        #     status=user.status
        # )
        return user

    # async def list_users(self, skip: int = 0, limit: int = 10) -> list[User]:
    #     return await crud.get_users(self.db, skip=skip, limit=limit)
