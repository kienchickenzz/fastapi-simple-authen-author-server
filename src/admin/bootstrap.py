"""
Auto-bootstrap admin user khi application startup.

Module này kiểm tra xem có admin user nào chưa, nếu chưa có thì
tự động tạo từ environment variables.
"""

import logging

from sqlalchemy.ext.asyncio import AsyncEngine

from src.config import Config
from src.admin.service import AdminService


logger = logging.getLogger("app")


class AdminBootstrap:
    """
    Auto-bootstrap admin user khi startup.

    Chỉ tạo admin khi:
    1. Chưa có user nào với Admin role trong database
    2. Có đủ ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD trong env

    Nếu thiếu config hoặc đã có admin, sẽ skip và log thông tin.
    """

    @staticmethod
    async def run(db_engine: AsyncEngine, config: Config) -> None:
        """
        Kiểm tra và tạo admin từ env nếu cần.

        Args:
            db_engine (AsyncEngine): Database engine đã khởi tạo.
            config (Config): Configuration object.
        """
        admin_service = await AdminService.create_instance(db_engine)

        # Kiểm tra đã có admin chưa
        if await admin_service.has_any_admin():
            logger.info("Admin user already exists, skipping bootstrap")
            return

        # Đọc credentials từ env
        username = config.get_config("ADMIN_USERNAME", "")
        email = config.get_config("ADMIN_EMAIL", "")
        password = config.get_config("ADMIN_PASSWORD", "")

        # Kiểm tra có đủ config không
        if not username or not email or not password:
            logger.warning(
                "No admin user found in database. "
                "To auto-bootstrap, set ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD in .env. "
                "Or use CLI: uv run python -m src admin:create"
            )
            return

        # Tạo admin
        try:
            user_id = await admin_service.create_admin(
                username=username,
                email=email,
                password=password,
            )
            logger.info(
                f"Admin user bootstrapped successfully: "
                f"username={username}, id={user_id}"
            )
        except ValueError as e:
            logger.error(f"Failed to bootstrap admin: {e}")
