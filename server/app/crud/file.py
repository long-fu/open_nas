# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from app.models.file import File, DirectoryClosure, MinioFile
# from sqlalchemy import select, insert, delete, and_

# # 创建目录（在 files 表中 is_directory = True），并维护闭包表


# async def create_directory(db: AsyncSession, owner_id: str, name: str, parent_id: int = None) -> File:
#     new = File(owner_id=owner_id, parent_id=parent_id,
#                name=name, type="文件夹", storage_path="", content_type="")
#     db.add(new)
#     await db.commit()
#     await db.refresh(new)
#     await insert_closure_for_new(db, new.id, parent_id)
#     return new

# # 创建文件元记录（不含上传）


# async def create_file_record(db: AsyncSession, owner_id: str, name: str, parent_id: int | None, storage_url: str, size: int, mime_type: str, type: str, hash: str):
#     new = File(owner_id=owner_id, parent_id=parent_id, name=name,
#                storage_url=storage_url, size=size, type="照片", content_type=mime_type, hash=hash)
#     db.add(new)
#     await db.commit()
#     await db.refresh(new)
#     await insert_closure_for_new(db, new.id, parent_id)
#     return new


# # list directory children

# async def list_children(db: AsyncSession, owner_id: str, dir_id: int):
#     q = select(File).where(File.parent_id == dir_id, File.owner_id == owner_id)
#     res = await db.execute(q)
#     return res.scalars().all()

# # get full path


# async def get_path(db: AsyncSession, file_id: int):
#     return await get_full_path(db, file_id)

# # move node


# async def move(db: AsyncSession, node_id: int, new_parent_id: int):
#     await move_node(db, node_id, new_parent_id)


# # 生成完整路径 via closure table
# async def get_full_path(db: AsyncSession, file_id: int) -> str:
#     # 查询所有祖先（ancestor）并按 depth 升序
#     q = select(File.name, DirectoryClosure.depth).join(
#         DirectoryClosure, DirectoryClosure.ancestor_id == File.id
#     ).where(DirectoryClosure.descendant_id == file_id).order_by(DirectoryClosure.depth.asc())
#     res = await db.execute(q)
#     rows = res.fetchall()
#     if not rows:
#         return ""
#     names = [r[0] for r in rows]
#     return "/" + "/".join(names)

# # 当新增节点（目录或文件）时，维护 closure 表
# # new_id: 插入后的文件id; parent_id: 父目录id (nullable)


# async def insert_closure_for_new(db: AsyncSession, new_id: int, parent_id: int = None):
#     # If parent is null -> root: insert (new,new,0)
#     if parent_id is None:
#         stmt = insert(DirectoryClosure).values(
#             ancestor_id=new_id, descendant_id=new_id, depth=0)
#         await db.execute(stmt)
#         await db.commit()
#         return
#     # Insert ancestor relationships copied from parent + self relation
#     # SELECT ancestor_id, parent_id, depth FROM closure WHERE descendant_id = parent_id
#     q = select(DirectoryClosure.ancestor_id, DirectoryClosure.depth).where(
#         DirectoryClosure.descendant_id == parent_id
#     )
#     res = await db.execute(q)
#     rows = res.fetchall()
#     # Build inserts: (ancestor_id, new_id, depth+1)
#     values = []
#     for ancestor_id, depth in rows:
#         values.append({"ancestor_id": ancestor_id,
#                       "descendant_id": new_id, "depth": depth + 1})
#     # add self
#     values.append({"ancestor_id": new_id, "descendant_id": new_id, "depth": 0})
#     if values:
#         await db.execute(insert(DirectoryClosure), values)
#         await db.commit()

# # Move node: change parent of node_id to new_parent_id
# # Implementation approach:
# # 1. delete closure entries where ancestor IN (old_ancestors) and descendant IN (subtree)
# # 2. insert new closure entries by combining new parent's ancestors with subtree nodes


# async def move_node(db: AsyncSession, node_id: int, new_parent_id: int):
#     # get all descendants of node (subtree)
#     q_desc = select(DirectoryClosure.descendant_id).where(
#         DirectoryClosure.ancestor_id == node_id)
#     res = await db.execute(q_desc)
#     descendants = [r[0] for r in res.fetchall()]

#     # get all ancestors of node (old ancestors)
#     q_anc = select(DirectoryClosure.ancestor_id).where(
#         DirectoryClosure.descendant_id == node_id)
#     res = await db.execute(q_anc)
#     old_ancestors = [r[0] for r in res.fetchall()]

#     # delete closure entries linking old ancestors to subtree
#     del_stmt = delete(DirectoryClosure).where(
#         and_(
#             DirectoryClosure.ancestor_id.in_(old_ancestors),
#             DirectoryClosure.descendant_id.in_(descendants)
#         )
#     )
#     await db.execute(del_stmt)

#     # get new parent's ancestors
#     q_newp = select(DirectoryClosure.ancestor_id, DirectoryClosure.depth).where(
#         DirectoryClosure.descendant_id == new_parent_id
#     )
#     res = await db.execute(q_newp)
#     newp_rows = res.fetchall()  # list of (ancestor_id, depth)

#     # get subtree nodes and their depth to node
#     q_sub = select(DirectoryClosure.descendant_id, DirectoryClosure.depth).where(
#         DirectoryClosure.ancestor_id == node_id
#     )
#     res = await db.execute(q_sub)
#     sub_rows = res.fetchall()  # list of (descendant_id, depth_to_node)
#     # build inserts: for each new ancestor A and subtree node S: (A, S, depth(A->newparent)+1 + depth(node->S))
#     values = []
#     for a_id, a_depth in newp_rows:
#         for s_id, s_depth in sub_rows:
#             values.append({
#                 "ancestor_id": a_id,
#                 "descendant_id": s_id,
#                 "depth": a_depth + 1 + s_depth
#             })
#     # also ensure subtree self-relations already exist (but we'll insert anyway)
#     # execute batch insert
#     if values:
#         await db.execute(insert(DirectoryClosure), values)
#     # update parent_id in file table
#     await db.execute(
#         select(File).where(File.id == node_id)
#     )  # just ensure node exists
#     await db.execute(
#         # update
#         File.__table__.update().where(File.id == node_id).values(parent_id=new_parent_id)
#     )
#     await db.commit()

# # 上传文件 endpoint helper


# async def upload_file(db: AsyncSession, owner_id: str, parent_id: int | None, upload_file: MinioFile):

#     rec = await create_file_record(db, owner_id, upload_file.file_name, parent_id, upload_file.url, upload_file.size, upload_file.content_type, upload_file.hash)

#     return rec

# # 上传文件 endpoint helper


# # async def upload_picture(db: AsyncSession, owner_id: int, parent_id: int, upload_file: UploadMinioFile):
# #     # make filename unique: ownerid_timestamp_original
# #     import time
# #     import uuid
# #     ext = os.path.splitext(upload_file.filename)[1]

# #     # 解析出路径

# #     # 解析图片格式信息

# #     # 查询dic，没有就进行创建

# #     safe_name = f"{owner_id}_{int(time.time())}_{uuid.uuid4().hex}{ext}"

# #     dest, size = await save_upload_file(upload_file, safe_name)

# #     mime = upload_file.content_type

# #     # create db record
# #     rec = await create_file_record(db, owner_id, upload_file.filename, parent_id, dest, size, mime)

# #     return rec
