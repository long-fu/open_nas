from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from app.database import Base, engine
from app.database import get_db
# from app.schemas.file import FileRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import file as crud
import asyncio
from app.routers.auth import get_current_user, api_key_header
from fastapi import Security
from fastapi import APIRouter, Depends
from app.services.file import FileService
from app.schemas.file import FileCreate, FileRead,FileTree
from typing import List,Optional

router = APIRouter(prefix="/files", tags=["File"])


@router.post("/", response_model=FileRead)
async def upload_file(upload: UploadFile = File(...), 
                      db: AsyncSession = Depends(get_db), 
                      api_key: str = Security(api_key_header)):
    # file = await create_file(db, file_in, current_user.id)
    uid = get_current_user(api_key)
    service = FileService(db)
    file = await service.upload_file(uid, upload)
    return file


@router.get("/", response_model=List[FileRead])
async def list_user_files(
    db: AsyncSession = Depends(get_db),
    api_key: str = Security(api_key_header)
):
    uid = get_current_user(api_key)
    service = FileService(db)
    files = await service.get_user_files(uid)
    return files


@router.get("/{parent_id}/children", response_model=List[FileRead])
async def list_children(
        parent_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: str = Security(api_key_header)
):
    uid = get_current_user(api_key)
    service = FileService(db)
    children = await service.get_children(parent_id)
    return children


@router.delete("/{file_id}")
async def remove_file(
        file_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: str = Security(api_key_header)
):
    uid = get_current_user(api_key)
    service = FileService(db)
    await service.delete_file(file_id)
    return {"message": "File and its descendants deleted successfully"}

@router.get("/{dir_id}/all", response_model=List[FileRead])
async def list_all_files_in_dir(
        dir_id: int,
    db: AsyncSession = Depends(get_db),
    api_key: str = Security(api_key_header)
):
    """
    递归列出指定目录下的所有文件
    """
    uid = get_current_user(api_key)
    service = FileService(db)
    files = await service.get_all_descendants(dir_id)
    return files

@router.get("/tree", response_model=List[FileTree])
async def get_directory_tree_api(
    dir_id: Optional[int] = None,  # ✅ 从query 参数获取数据 可以为空
    db: AsyncSession = Depends(get_db),
    api_key: str = Security(api_key_header)
):
    """
    获取文件树结构
    - 如果 dir_id 为空：从根目录 (parent_id IS NULL) 开始
    - 如果 dir_id 有值：查询该目录下的所有子项
    """
    uid = get_current_user(api_key)
    service = FileService(db)    
    tree = await service.get_directory_tree(dir_id)
    return tree

# @router.post("/dirs", response_model=FileOut)
# async def api_create_dir(payload: FileCreate, db: AsyncSession = Depends(get_db), api_key: str = Security(api_key_header)):
#     uid = get_current_user(api_key)
#     service = FileService(db)
#     f = await service.create_directory(uid, payload.name, payload.parent_id)
#     return f

# @router.post("/upload", response_model=FileRead)
# async def api_upload(upload: UploadFile = File(...), db: AsyncSession = Depends(get_db), api_key: str = Security(api_key_header)):
#     uid = get_current_user(api_key)
#     service = FileService(db)
#     rec = await service.upload_file(uid, upload)
#     return rec

# @router.get("/{file_id}/path")
# async def api_get_path(file_id: int, db: AsyncSession = Depends(get_db)):
#     service = FileService(db)
#     path = await service.get_path(file_id)

#     if not path:
#         raise HTTPException(status_code=404, detail="Not found")
#     return {"path": path}

# @router.get("/dirs/{dir_id}/children")
# async def api_list_children(dir_id: int, db: AsyncSession = Depends(get_db), api_key: str = Security(api_key_header)):
#     uid = get_current_user(api_key)
#     service = FileService(db)
#     items = await service.list_children(uid, dir_id)
#     return items

# @router.post("/files/{file_id}/move")
# async def api_move(file_id: int, new_parent: int, db: AsyncSession = Depends(get_db)):
#     await crud.move(db, file_id, new_parent)
#     return {"ok": True}
