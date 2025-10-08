from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.file import DFile, DirectoryClosure, MinioFile
from sqlalchemy import select, insert, delete, and_
from typing import List
from app.services.file import FileCreate
from sqlalchemy.exc import IntegrityError
# 创建目录（在 files 表中 is_directory = True），并维护闭包表

# 创建文件或目录
async def create_file(db: AsyncSession, file_in: FileCreate, owner_id: str):
    
    q = select(DFile).where(DFile.owner_id == owner_id, DFile.parent_id == file_in.parent_id, DFile.name == file_in.name)
    result = await db.execute(q)
    existing = result.scalar_one_or_none()
    # existing = result.scalars().first()
    if existing:
        return existing
    
    file = DFile(**file_in.model_dump(), owner_id=owner_id)
    db.add(file)
    
    try:
        await db.flush()  # 让 SQLAlchemy 获取 file.id
        
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
        return file        
    except IntegrityError:
        db.rollback()
        raise ValueError("文件或目录已存在")
        return None
    



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

# 获取某个目录下的所有子文件（递归）
async def get_all_descendants(db: AsyncSession, dir_id: int):
    """
    返回指定目录下的所有文件（包括子目录递归层级）
    """
    result = await db.execute(
        select(DFile)
        .join(DirectoryClosure, DirectoryClosure.descendant_id == DFile.id)
        .where(DirectoryClosure.ancestor_id == dir_id, DirectoryClosure.depth > 0)
    )
    return result.scalars().all()

async def get_directory_tree(db: AsyncSession, dir_id: int | None = None):
    """
    从指定目录（或根目录）开始递归获取文件树
    """
    if dir_id is None:
        query = select(DFile).where(DFile.parent_id.is_(None))  # 根目录
    else:
        query = select(DFile).where(DFile.parent_id == dir_id)  # 指定目录
    result = await db.execute(query)
    children = result.scalars().all()
    tree = []
    for child in children:
        node = {
            "id": child.id,
            "name": child.name,
            "content_type": child.content_type,
            "size": child.size,
            "hash": child.hash,
            "storage_url": child.storage_url,
            "children": []
        }
        if child.size == 0:  # 目录
            node["children"] = await get_directory_tree(db, child.id)
        tree.append(node)
    return tree