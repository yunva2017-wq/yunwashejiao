"""
好友 Schema
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FriendRequestCreate(BaseModel):
    addressee_username: str
    remark: Optional[str] = None  # 备注信息


class FriendRequestResponse(BaseModel):
    id: int
    requester_id: int
    addressee_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FriendResponse(BaseModel):
    id: int
    user_id: int
    username: str
    nickname: Optional[str]
    avatar: str
    remark: Optional[str]  # 好友备注
    status: str

    class Config:
        from_attributes = True
