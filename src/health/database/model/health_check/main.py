from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class HealthCheck(Base):
    __tablename__ = "health_check"

    def __repr__(self) -> str:
        return f"HealthCheck()"
