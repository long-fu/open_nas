from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User

async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, name: str, email: str):
    new_user = User(name=name, email=email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
