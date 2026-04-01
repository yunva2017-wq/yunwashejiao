"""
好友服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from ..models.friendship import Friendship, FriendStatus
from ..models.user import User
from ..schemas.friendship import FriendRequestCreate


def search_users(db: Session, query: str, current_user_id: int, limit: int = 20):
    """搜索用户"""
    result = db.execute(
        select(User)
        .where(User.username.contains(query))
        .where(User.id != current_user_id)
        .limit(limit)
    )
    return result.scalars().all()


def get_friend_requests(db: Session, user_id: int):
    """获取好友请求列表"""
    # 别人发给我的请求
    incoming = db.execute(
        select(Friendship)
        .where(Friendship.addressee_id == user_id)
        .where(Friendship.status == FriendStatus.PENDING)
    ).scalars().all()
    return incoming


def get_friends(db: Session, user_id: int):
    """获取好友列表"""
    # 我发起的已接受请求 + 别人发起的已接受请求
    friends = db.execute(
        select(Friendship)
        .where(Friendship.status == FriendStatus.ACCEPTED)
        .where(
            or_(
                Friendship.requester_id == user_id,
                Friendship.addressee_id == user_id
            )
        )
    ).scalars().all()
    return friends


def create_friend_request(db: Session, requester_id: int, addressee_username: str):
    """创建好友请求"""
    # 查找目标用户
    addressee = db.execute(
        select(User).where(User.username == addressee_username)
    ).scalar_one_or_none()

    if not addressee:
        return None, "user_not_found"

    if addressee.id == requester_id:
        return None, "cannot_add_self"

    # 检查是否已经是好友
    existing = db.execute(
        select(Friendship)
        .where(
            or_(
                (Friendship.requester_id == requester_id) & (Friendship.addressee_id == addressee.id),
                (Friendship.requester_id == addressee.id) & (Friendship.addressee_id == requester_id)
            )
        )
        .where(Friendship.status == FriendStatus.ACCEPTED)
    ).scalar_one_or_none()

    if existing:
        return None, "already_friends"

    # 检查是否有待处理的请求
    pending = db.execute(
        select(Friendship)
        .where(
            (Friendship.requester_id == requester_id) &
            (Friendship.addressee_id == addressee.id) &
            (Friendship.status == FriendStatus.PENDING)
        )
    ).scalar_one_or_none()

    if pending:
        return None, "request_pending"

    # 创建好友请求
    friendship = Friendship(
        requester_id=requester_id,
        addressee_id=addressee.id,
        status=FriendStatus.PENDING
    )
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship, None


def respond_to_request(db: Session, request_id: int, user_id: int, accept: bool):
    """响应好友请求"""
    friendship = db.execute(
        select(Friendship).where(Friendship.id == request_id)
    ).scalar_one_or_none()

    if not friendship:
        return None, "request_not_found"

    if friendship.addressee_id != user_id:
        return None, "not_your_request"

    if friendship.status != FriendStatus.PENDING:
        return None, "request_already_processed"

    if accept:
        friendship.status = FriendStatus.ACCEPTED
    else:
        # 拒绝则删除
        db.delete(friendship)

    db.commit()
    return friendship, None


def remove_friend(db: Session, user_id: int, friend_id: int):
    """删除好友"""
    friendship = db.execute(
        select(Friendship)
        .where(Friendship.status == FriendStatus.ACCEPTED)
        .where(
            or_(
                (Friendship.requester_id == user_id) & (Friendship.addressee_id == friend_id),
                (Friendship.requester_id == friend_id) & (Friendship.addressee_id == user_id)
            )
        )
    ).scalar_one_or_none()

    if not friendship:
        return False

    db.delete(friendship)
    db.commit()
    return True


def get_friend_by_user_id(db: Session, user_id: int, friend_id: int):
    """获取特定好友关系"""
    friendship = db.execute(
        select(Friendship)
        .where(Friendship.status == FriendStatus.ACCEPTED)
        .where(
            or_(
                (Friendship.requester_id == user_id) & (Friendship.addressee_id == friend_id),
                (Friendship.requester_id == friend_id) & (Friendship.addressee_id == user_id)
            )
        )
    ).scalar_one_or_none()
    return friendship
