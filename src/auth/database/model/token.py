"""
Model đại diện cho bảng tokens trong database.
"""
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class Token(Base):
    """
    Model lưu trữ các JWT tokens đã phát hành.

    Args:
        user_id (int): ID của user sở hữu token.
        token (str): JWT token string.
        is_active (bool): Trạng thái token (True=active, False=revoked).
        expired_at (datetime): Thời gian token hết hạn.
    """

    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
