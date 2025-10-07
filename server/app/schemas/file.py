# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

# class FileCreate(BaseModel):
#     name: str
#     parent_id: Optional[int]
#     is_directory: bool = False

# class FileOut(BaseModel):
#     id: int
#     name: str
#     parent_id: Optional[int]
#     owner_id: int
#     storage_url: str
#     size: int
#     hash: str
#     created_at: Optional[datetime]
#     class Config:
#         orm_mode = True