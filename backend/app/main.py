"""
云娃聊天应用 - 主入口
功能：用户注册、文字聊天、语音聊天
"""
import asyncio
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import socketio
from datetime import datetime

from .models.database import engine, Base, get_db
from .models.user import User
from .models.message import Message
from .models.friendship import Friendship  # 新增好友模型
from .schemas.user import UserCreate, UserLogin, UserResponse
from .schemas.message import MessageCreate, MessageResponse
from .services.auth import get_current_user, create_access_token, verify_token
from .services.user import create_user, get_user_by_username
from .utils.config import settings

# 数据库初始化
Base.metadata.create_all(bind=engine)

# FastAPI 应用
app = FastAPI(
    title="云娃聊天",
    description="实时社交聊天应用 - 支持文字和语音聊天",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件（语音消息存储）
app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")

# Socket.IO 配置
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# 在线用户管理
online_users = {}


# ==================== 用户接口 ====================

@app.post("/api/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 创建用户
    user = create_user(db, user_data)
    return user


@app.post("/api/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = get_user_by_username(db, user_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 验证密码
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 生成 token
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "user": user}


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户信息"""
    from sqlalchemy import select
    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


# ==================== 消息接口 ====================

@app.get("/api/messages/{room_id}", response_model=List[MessageResponse])
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


@app.post("/api/upload-voice", status_code=status.HTTP_201_CREATED)
async def upload_voice(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传语音消息"""
    import os
    import uuid

    # 生成唯一文件名
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "webm"
    filename = f"{uuid.uuid4()}.{file_extension}"
    filepath = f"static/uploads/voice/{filename}"

    # 确保目录存在
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # 保存文件
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"url": f"/uploads/voice/{filename}", "filename": filename}


# ==================== WebSocket/Socket.IO 事件 ====================

@sio.event
async def connect(sid, environ):
    """用户连接"""
    print(f"用户连接：{sid}")


@sio.event
async def disconnect(sid):
    """用户断开连接"""
    print(f"用户断开：{sid}")
    # 从在线用户中移除
    if sid in online_users:
        del online_users[sid]
        # 通知其他人该用户下线
        await sio.emit("user_offline", {"username": online_users.get(sid)})


@sio.on("join")
async def join_room(sid, data):
    """加入聊天室"""
    username = data.get("username")
    room_id = data.get("room_id")
    token = data.get("token")

    # 验证 token
    user_data = verify_token(token)
    if not user_data:
        await sio.emit("error", {"message": "认证失败"}, room=sid)
        return

    # 加入房间
    await sio.enter_room(sid, room_id)
    online_users[sid] = username

    # 通知房间内其他人
    await sio.emit("user_online", {"username": username}, room=room_id, skip_sid=sid)

    # 发送成功消息
    await sio.emit("joined", {"room_id": room_id, "username": username}, room=sid)


@sio.on("chat_message")
async def send_message(sid, data):
    """发送聊天消息"""
    room_id = data.get("room_id")
    message_data = data.get("message")

    # 广播消息给房间内所有人
    await sio.emit("new_message", message_data, room=room_id)


@sio.on("voice_call")
async def voice_call(sid, data):
    """发起语音通话"""
    target_id = data.get("target_id")
    call_data = {
        "caller": data.get("caller"),
        "room_id": data.get("room_id"),
        "type": "voice"
    }

    # 通知被呼叫方
    await sio.emit("incoming_call", call_data, room=target_id)


@sio.on("call_accept")
async def call_accept(sid, data):
    """接受通话"""
    caller_id = data.get("caller_id")
    await sio.emit("call_accepted", {"accepted_by": data.get("accepted_by")}, room=caller_id)


@sio.on("call_reject")
async def call_reject(sid, data):
    """拒绝通话"""
    caller_id = data.get("caller_id")
    await sio.emit("call_rejected", {}, room=caller_id)


@sio.on("call_end")
async def call_end(sid, data):
    """结束通话"""
    target_id = data.get("target_id")
    await sio.emit("call_ended", {}, room=target_id)


@sio.on("webrtc_offer")
async def webrtc_offer(sid, data):
    """WebRTC Offer"""
    target_id = data.get("target_id")
    await sio.emit("webrtc_offer", {
        "offer": data.get("offer"),
        "caller": data.get("caller")
    }, room=target_id)


@sio.on("webrtc_answer")
async def webrtc_answer(sid, data):
    """WebRTC Answer"""
    target_id = data.get("target_id")
    await sio.emit("webrtc_answer", {
        "answer": data.get("answer"),
        "caller": data.get("caller")
    }, room=target_id)


@sio.on("ice_candidate")
async def ice_candidate(sid, data):
    """ICE Candidate"""
    target_id = data.get("target_id")
    await sio.emit("ice_candidate", {
        "candidate": data.get("candidate"),
        "caller": data.get("caller")
    }, room=target_id)


# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# ==================== 好友接口 ====================

from .api.friends import router as friends_router
app.include_router(friends_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
