"""
数据库配置
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..utils.config import settings

# 数据库 URL
DATABASE_URL = settings.database_url

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.debug
)

# Session 配置
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
