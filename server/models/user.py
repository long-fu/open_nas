from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "tb_users"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(64), unique=True)
    name = Column(String(64))
    email = Column(String(100), unique=True)
    phone = Column(String(100), unique=True)
