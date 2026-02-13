"""
Model đại diện cho bảng users trong database.
"""
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class User(Base):
    """
    Model user trong hệ thống.

    Args:
        username (str): Tên đăng nhập, unique.
        email (str): Email, unique.
        password_hash (str): Mật khẩu đã hash.
        is_active (bool): Trạng thái hoạt động.
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
