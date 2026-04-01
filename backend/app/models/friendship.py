"""
好友关系模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from datetime import datetime
from .database import Base
import enum


class FriendStatus(str, enum.Enum):
    PENDING = "pending"      # 等待对方同意
    ACCEPTED = "accepted"    # 已是好友
    BLOCKED = "blocked"      # 已拉黑


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 发起方
    addressee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 接收方
    status = Column(String(20), default=FriendStatus.PENDING, nullable=False)  # pending, accepted, blocked
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Friendship {self.requester_id} -> {self.addressee_id} ({self.status})>"
