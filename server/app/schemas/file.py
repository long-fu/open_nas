from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FileBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    # type: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = 0
    hash: Optional[str] = None
    storage_url: Optional[str] = None

class FileCreate(FileBase):
    pass

class FileRead(FileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DirectoryTree(BaseModel):
    id: int
    name: str
    children: List["DirectoryTree"] = []
    class Config:
        orm_mode = True

class FileTree(FileBase):
    id: int
    name: str
    children: List["FileTree"] = []
    class Config:
        orm_mode = True