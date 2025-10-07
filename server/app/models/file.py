from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, TIMESTAMP, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.types import TypeDecorator, Integer
from sqlalchemy.sql import func

# 临时存储
class MinioFile:
    url:str = ''
    file_name: str = ''
    bucket_name: str = ''
    object_name: str = ''
    size: int = 0
    content_type: str = ''
    hash: str = ''

class FileType(TypeDecorator):
    impl = Integer
    FILE_TYPE_MAP = {0: "目录", 1: "照片", 2: "视频", 3: "文档", 4: "音频", 5: "文件"}
    FILE_TYPE_REVERSE_MAP = {v: k for k, v in FILE_TYPE_MAP.items()}

    def process_bind_param(self, value, dialect):
        if value is None:
            return 0  # 默认文件
        return self.FILE_TYPE_REVERSE_MAP[value]

    def process_result_value(self, value, dialect):
        if value is None:
            return "目录"
        return self.FILE_TYPE_MAP[value]



class File(Base):
    __tablename__ = "files"
    
    # 主键ID
    id = Column(BigInteger, primary_key=True, index=True)
    
    # 文件/目录所属用户
    owner_id = Column(String(256), ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    
    # 父目录ID（自关联 files.id）
    parent_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), nullable=True)
    
    # 文件名或目录名
    name = Column(String(512), nullable=False)
    
    size = Column(BigInteger, default=0)
    
    type = Column(FileType(), nullable=False)
    
    hash = Column(String(256), nullable=False)
    
    storage_url = Column(Text, nullable=False)

    # 创建时间
    created_at = Column(TIMESTAMP, server_default=func.now())

    # 更新时间
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="files")
    # ✅ ORM 自引用关系
    # children 表示当前目录的所有子文件/子目录（仅一层）
    # backref="parent" 表示反向访问父目录对象，例如 file.parent
    # remote_side=[id] 告诉 SQLAlchemy parent_id 指向本表的 id 列
    children = relationship("File", cascade="all, delete", backref="parent", remote_side=[id])

class DirectoryClosure(Base):
    __tablename__ = "directory_closure"
    ancestor_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), primary_key=True)
    descendant_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), primary_key=True)
    depth = Column(Integer, nullable=False)
    

