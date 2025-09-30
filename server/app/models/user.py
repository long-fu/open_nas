from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import TIMESTAMP, text
from sqlalchemy import Enum
import datetime
from sqlalchemy.types import TypeDecorator, Integer
from sqlalchemy import Column, Date

# 数据库存储映射


class GenderType(TypeDecorator):
    impl = Integer
    GENDER_MAP = {0: "男", 1: "女", 2: "未知"}
    GENDER_REVERSE_MAP = {v: k for k, v in GENDER_MAP.items()}

    def process_bind_param(self, value, dialect):
        if value is None:
            return 2  # 默认未知
        return self.GENDER_REVERSE_MAP[value]

    def process_result_value(self, value, dialect):
        if value is None:
            return "未知"
        return self.GENDER_MAP[value]

# 数据库存储映射


class StatusType(TypeDecorator):
    impl = Integer

    STATUS_MAP = {0: "禁用", 1: "正常"}
    STATUS_REVERSE_MAP = {v: k for k, v in STATUS_MAP.items()}

    def process_bind_param(self, value, dialect):
        # Python -> 数据库
        if value is None:
            return 1  # 默认正常
        return self.STATUS_REVERSE_MAP[value]

    def process_result_value(self, value, dialect):
        # 数据库 -> Python
        if value is None:
            return "正常"
        return self.STATUS_MAP[value]


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(String, unique=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(GenderType(), nullable=False)
    birthdate = Column(Date, nullable=True)
    status = Column(StatusType(), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text(
        "CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
