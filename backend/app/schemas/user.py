"""
用户 Schema
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    nickname: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, description="邮箱地址")
    phone: Optional[str] = None

    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, v):
        if not v or v.strip() == '':
            return None
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    avatar: str = "/uploads/avatar/default.png"
    created_at: datetime

    class Config:
        from_attributes = True
