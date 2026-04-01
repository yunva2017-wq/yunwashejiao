"""
应用配置
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 应用配置
    app_name: str = "云娃聊天"
    debug: bool = True
    secret_key: str = "glimmer-chat-secret-key-2026-change-in-production"

    # 数据库配置
    database_url: str = "postgresql://postgres:postgres@localhost:5432/glimmer_chat"

    # JWT 配置
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 天

    class Config:
        env_file = ".env"


settings = Settings()
