import asyncio
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import user

app = FastAPI(title="FastAPI Async MVC User Service")
app.include_router(user.router)

# 异步创建表
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())
