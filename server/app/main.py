from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth
from app.routers import user
from app.routers import file
app = FastAPI(title="FastAPI Async Auth MVC")
app.include_router(auth.router)
app.include_router(user.router)
# app.include_router(file.router)
# 异步创建表
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 在 FastAPI 启动时调用
@app.on_event("startup")
async def on_startup():
    await init_models()
