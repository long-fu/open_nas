from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.services.user import UserService
from app.database import get_db
from fastapi import FastAPI, Form, File, UploadFile

router = APIRouter()

# @router.post("/upload/",     username: str = Form(...),                # 表单字段
#     description: str = Form(""),              # 可选字段，有默认值
#     file: UploadFile = File(...)              # 文件字段)
# async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     service = UserService(db)
#     return await service.create_user(user)

# 上传接口
# @router.post("/upload_image/")
# async def upload_file(
#     username: str = Form(...),                # 表单字段
#     description: str = Form(""),              # 可选字段，有默认值
#     file: UploadFile = File(...)              # 文件字段
# ):
#     # 读取文件内容（注意：大文件不建议直接 read()）
#     content = await file.read()
    
#     return JSONResponse({
#         "filename": file.filename,
#         "content_type": file.content_type,
#         "username": username,
#         "description": description,
#         "file_size": len(content)
#     })