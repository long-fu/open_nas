from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from models.user import Base
from routers import user_router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时清理连接
    await engine.dispose()

app = FastAPI(title="FastAPI Async MVC Example", lifespan=lifespan)
app.include_router(user_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)