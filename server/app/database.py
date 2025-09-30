# from config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# # 创建异步数据库引擎
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True,  # 输出 SQL 日志，可选
# )

# # 异步 Session
# AsyncSessionLocal = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )

# Base = declarative_base()

# # 异步依赖注入
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

DATABASE_URL = "postgresql+asyncpg://postgres:Haoshuai9291.@127.0.0.1/open_nas_db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 异步依赖注入
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session