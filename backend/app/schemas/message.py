"""
消息 Schema
"""
from pydantic import BaseModel, Field
from datetime import datetime


class MessageBase(BaseModel):
    message_type: str = "text"  # text, voice, image
    content: str


class MessageCreate(MessageBase):
    room_id: str
    sender_id: int
    sender_username: str


class MessageResponse(MessageBase):
    id: int
    room_id: str
    sender_id: int
    sender_username: str
    created_at: datetime

    class Config:
        from_attributes = True
