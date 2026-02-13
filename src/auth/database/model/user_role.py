from sqlalchemy import ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
