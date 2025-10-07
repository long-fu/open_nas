from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.file import DFile, DirectoryClosure, MinioFile
from sqlalchemy import select, insert, delete, and_
from typing import List
from app.services.file import FileCreate
# 创建目录（在 files 表中 is_directory = True），并维护闭包表

# 创建文件或目录
async def create_file(db: AsyncSession, file_in: FileCreate, owner_id: str):
    file = DFile(**file_in.model_dump(), owner_id=owner_id)
    db.add(file)
    await db.flush()  # 让 SQLAlchemy 获取 file.id
    # print("111111111111111111111")
    # print(file.id)
    # 插入自己到 closure 表 (自反路径)
    db.add(DirectoryClosure(ancestor_id=file.id, descendant_id=file.id, depth=0))

    # 如果有 parent_id，则复制父节点的所有祖先路径 + 自己
    if file_in.parent_id:
        parent_paths = await db.execute(
            select(DirectoryClosure).where(DirectoryClosure.descendant_id == file_in.parent_id)
        )
        for path in parent_paths.scalars().all():
            db.add(DirectoryClosure(
                ancestor_id=path.ancestor_id,
                descendant_id=file.id,
                depth=path.depth + 1
            ))

    await db.commit()
    await db.refresh(file)
    # print(file.id)
    return file


# 获取用户所有文件
async def get_user_files(db: AsyncSession, owner_id: str) -> List[DFile]:
    result = await db.execute(select(DFile).where(DFile.owner_id == owner_id))
    return result.scalars().all()


# 获取某目录下的子文件
async def get_children(db: AsyncSession, parent_id: int):
    result = await db.execute(select(DFile).where(DFile.parent_id == parent_id))
    return result.scalars().all()


# 删除文件及所有子文件
async def delete_file(db: AsyncSession, file_id: int):
    # 找到所有后代节点
    result = await db.execute(
        select(DirectoryClosure.descendant_id).where(DirectoryClosure.ancestor_id == file_id)
    )
    descendants = [r[0] for r in result.all()]
    await db.execute(delete(DFile).where(DFile.id.in_(descendants)))
    await db.commit()