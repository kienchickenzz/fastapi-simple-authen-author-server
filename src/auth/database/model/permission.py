"""
Model đại diện cho bảng permissions trong database.
"""
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class Permission(Base):
    """
    Model permission trong hệ thống phân quyền.

    Args:
        code (str): Mã permission (e.g. "book:read"), unique.
        description (str | None): Mô tả permission.
    """

    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
