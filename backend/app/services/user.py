"""
用户服务
"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import User
from ..schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str) -> User | None:
    """根据用户名获取用户"""
    from sqlalchemy import select
    result = db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    """根据邮箱获取用户"""
    from sqlalchemy import select
    result = db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


def create_user(db: Session, user_data: UserCreate) -> User:
    """创建用户"""
    password_hash = pwd_context.hash(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email if hasattr(user_data, 'email') else None,
        password_hash=password_hash,
        nickname=user_data.nickname if hasattr(user_data, 'nickname') else user_data.username
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """认证用户"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.password_hash):
        return None
    return user
