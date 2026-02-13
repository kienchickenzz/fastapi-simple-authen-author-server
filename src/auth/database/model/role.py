"""
Model đại diện cho bảng roles trong database.
"""
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class Role(Base):
    """
    Model role trong hệ thống phân quyền.

    Args:
        name (str): Tên role, unique.
        description (str | None): Mô tả role.
    """

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
