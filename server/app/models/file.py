from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, TIMESTAMP, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.types import TypeDecorator, Integer
from sqlalchemy.sql import func
from pydantic import BaseModel
# 临时存储
class MinioFile(BaseModel):
    url:str = ''
    file_name: str = ''
    bucket_name: str = ''
    object_name: str = ''
    size: int = 0
    content_type: str = ''
    file_hash: str = ''

class FileType(TypeDecorator):
    impl = Integer
    FILE_TYPE_MAP = {0: "文件夹", 1: "照片", 2: "视频", 3: "文档", 4: "音频", 5: "文件"}
    FILE_TYPE_REVERSE_MAP = {v: k for k, v in FILE_TYPE_MAP.items()}

    def process_bind_param(self, value, dialect):
        if value is None:
            return 0  # 默认文件
        return self.FILE_TYPE_REVERSE_MAP[value]

    def process_result_value(self, value, dialect):
        if value is None:
            return "目录"
        return self.FILE_TYPE_MAP[value]


# class FileBase()

class DFile(Base):
    __tablename__ = "files"
    
    # 主键ID
    id = Column(BigInteger, primary_key=True, index=True)
    
    # 文件/目录所属用户
    owner_id = Column(String, ForeignKey("users.uid", ondelete="CASCADE"), nullable=False, index=True)
    
    # 父目录ID（自关联 files.id）
    parent_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), nullable=True)
    
    # 文件名或目录名
    name = Column(String(512), nullable=False)
    
    
    size = Column(BigInteger, default=0)
    
    hash = Column(String(256), nullable=True)
    
    storage_url = Column(Text, nullable=True)
    
    # type = Column(FileType(), nullable=True)
    
    content_type = Column(String(256), nullable=True)
    
    # 创建时间
    created_at = Column(TIMESTAMP, server_default=func.now())

    # 更新时间
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 一对多关系
    owner = relationship("User", back_populates="files")
    
    # 层级关系
    ancestors = relationship(
            "DirectoryClosure",
        foreign_keys="[DirectoryClosure.descendant_id]",
        back_populates="descendant",
        cascade="all, delete"
    )

    descendants = relationship(
            "DirectoryClosure",
        foreign_keys="[DirectoryClosure.ancestor_id]",
        back_populates="ancestor",
        cascade="all, delete"
    )
    
    __table_args__ = (
        UniqueConstraint('owner_id', 'parent_id', 'name', name='uq_user_parent_name'),
    )


class DirectoryClosure(Base):
    __tablename__ = "directory_closure"

    ancestor_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), primary_key=True)
    descendant_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), primary_key=True)
    depth = Column(Integer, nullable=False)

    ancestor = relationship("DFile", foreign_keys=[ancestor_id], back_populates="descendants")
    descendant = relationship("DFile", foreign_keys=[descendant_id], back_populates="ancestors")

