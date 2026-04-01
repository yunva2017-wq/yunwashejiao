"""
好友 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..models.user import User
from ..schemas.user import UserResponse
from ..schemas.friendship import FriendRequestCreate, FriendRequestResponse, FriendResponse
from ..services.friendship import (
    search_users as search_users_service,
    get_friend_requests,
    get_friends,
    create_friend_request,
    respond_to_request,
    remove_friend,
    get_friend_by_user_id
)
from ..services.auth import get_current_user

router = APIRouter(prefix="/api/friends", tags=["好友"])


@router.get("/search")
async def search_users(
    q: str,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """搜索用户"""
    if not q or len(q) < 1:
        return []
    users = search_users_service(db, q, current_user.id, limit)
    return users


@router.get("/requests")
async def get_friend_requests_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取好友请求列表"""
    requests = get_friend_requests(db, current_user.id)
    return requests


@router.post("/requests")
async def send_friend_request(
    data: FriendRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发送好友请求"""
    friendship, error = create_friend_request(db, current_user.id, data.addressee_username)

    if error:
        error_messages = {
            "user_not_found": "用户不存在",
            "cannot_add_self": "不能添加自己为好友",
            "already_friends": "已经是好友了",
            "request_pending": "好友请求已发送，等待对方同意"
        }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_messages.get(error, "操作失败")
        )

    return {"message": "好友请求已发送", "request": friendship}


@router.post("/requests/{request_id}/respond")
async def respond_friend_request(
    request_id: int,
    accept: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """响应好友请求"""
    friendship, error = respond_to_request(db, request_id, current_user.id, accept)

    if error:
        error_messages = {
            "request_not_found": "请求不存在",
            "not_your_request": "这不是你的好友请求",
            "request_already_processed": "请求已处理"
        }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_messages.get(error, "操作失败")
        )

    if accept:
        return {"message": "已添加为好友"}
    else:
        return {"message": "已拒绝好友请求"}


@router.get("")
async def get_friend_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取好友列表"""
    friendships = get_friends(db, current_user.id)

    # 构建好友列表（包含对方用户信息）
    friends = []
    for f in friendships:
        friend_id = f.addressee_id if f.requester_id == current_user.id else f.requester_id
        friend_user = db.get(User, friend_id)
        if friend_user:
            friends.append({
                "id": f.id,
                "user_id": friend_user.id,
                "username": friend_user.username,
                "nickname": friend_user.nickname,
                "avatar": friend_user.avatar,
                "remark": None,
                "status": f.status
            })

    return friends


@router.delete("/{friend_id}")
async def delete_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除好友"""
    success = remove_friend(db, current_user.id, friend_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="好友关系不存在"
        )

    return {"message": "已删除好友"}


@router.get("/room/{friend_id}")
async def get_chat_room(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取与好友的聊天室 ID"""
    # 确认好友关系
    friendship = get_friend_by_user_id(db, current_user.id, friend_id)
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="不是好友关系"
        )

    # 生成唯一的聊天室 ID（格式：private_{user1_id}_{user2_id}，user1_id < user2_id）
    user_ids = sorted([current_user.id, friend_id])
    room_id = f"private_{user_ids[0]}_{user_ids[1]}"

    return {"room_id": room_id, "friend_id": friend_id}
