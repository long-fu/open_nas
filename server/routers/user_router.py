from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.database import get_session
from app.services.user_service import register_user
from app.crud.user import get_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def create_user_endpoint(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    return await register_user(session, name=user.name, email=user.email)

@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    db_user = await get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
