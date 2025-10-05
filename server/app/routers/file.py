from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from app.database import Base, engine
from app.database import get_db
from app.schemas.file import FileOut, FileCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import file as crud
import asyncio
from app.routers.auth import get_current_user, api_key_header
from fastapi import Security
from fastapi import APIRouter, Depends
from app.services.file import FileService
router = APIRouter(prefix="/file", tags=["User"])

@router.post("/dirs", response_model=FileOut)
async def api_create_dir(payload: FileCreate, db: AsyncSession = Depends(get_db), api_key: str = Security(api_key_header)):
    uid = get_current_user(api_key)
    service = FileService(db)
    f = await service.create_directory(uid, payload.name, payload.parent_id)
    return f

@router.post("/upload", response_model=FileOut)
async def api_upload(upload: UploadFile = File(...), db: AsyncSession = Depends(get_db), api_key: str = Security(api_key_header)):
    uid = get_current_user(api_key)
    service = FileService(db)
    rec = await service.upload_file(uid, upload)
    return rec

@router.get("/files/{file_id}/path")
async def api_get_path(file_id: int, db: AsyncSession = Depends(get_db)):
    service = FileService(db)
    path = await service.get_path(file_id)
    
    if not path:
        raise HTTPException(status_code=404, detail="Not found")
    return {"path": path}

@router.get("/dirs/{dir_id}/children")
async def api_list_children(dir_id: int, db: AsyncSession = Depends(get_db), api_key: str = Security(api_key_header)):
    uid = get_current_user(api_key)
    service = FileService(db)
    items = await service.list_children(uid, dir_id)
    return items

# @router.post("/files/{file_id}/move")
# async def api_move(file_id: int, new_parent: int, db: AsyncSession = Depends(get_db)):
#     await crud.move(db, file_id, new_parent)
#     return {"ok": True}