"""
消息 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

from ..models.database import get_db
from ..models.message import Message
from ..schemas.message import MessageCreate, MessageResponse
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/api", tags=["消息"])


@router.get("/messages/{room_id}", response_model=List[MessageResponse])
async def get_messages(room_id: str, limit: int = 50, db: Session = Depends(get_db)):
    """获取聊天室消息"""
    from sqlalchemy import select
    result = db.execute(
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = result.scalars().all()
    return list(reversed(messages))


@router.post("/upload-voice")
async def upload_voice(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传语音消息"""
    # 生成唯一文件名
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "webm"
    filename = f"{uuid.uuid4()}.{file_extension}"
    filepath = f"backend/static/uploads/voice/{filename}"

    # 确保目录存在
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # 保存文件
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"url": f"/uploads/voice/{filename}", "filename": filename}
