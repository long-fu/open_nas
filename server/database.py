from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import DATABASE_URL

# 异步 engine
engine = create_async_engine(DATABASE_URL, echo=True)

# 异步 session 工厂
async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# 异步生成器依赖注入
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
