"""
Service xử lý business logic cho Permission.
"""

from src.permission.database.repository.permission_repository import PermissionRepository
from src.permission.dto.permission_dto import (
    PermissionCreateRequest,
    PermissionResponse,
    PermissionListResponse,
)


class PermissionService:
    """
    Service cho Permission operations.

    Args:
        permission_repository (PermissionRepository): Repository để truy cập DB.
    """

    def __init__(self, permission_repository: PermissionRepository):
        """
        Khởi tạo PermissionService.

        Args:
            permission_repository (PermissionRepository): Repository để truy cập DB.
        """
        self._repository = permission_repository

    async def create(self, request: PermissionCreateRequest) -> PermissionResponse:
        """
        Tạo permission mới.

        Args:
            request (PermissionCreateRequest): Thông tin permission cần tạo.

        Returns:
            PermissionResponse: Permission đã tạo.
        """
        values = {
            "code": request.code,
            "description": request.description,
        }
        permission = await self._repository.create(values)
        return PermissionResponse(**permission.__dict__)

    async def get_list(self, target_page: int, page_size: int) -> PermissionListResponse:
        """
        Lấy danh sách permissions với phân trang.

        Args:
            target_page (int): Trang cần lấy.
            page_size (int): Số lượng mỗi trang.

        Returns:
            PermissionListResponse: Danh sách permissions.
        """
        skip = (target_page - 1) * page_size
        permissions, total = await self._repository.get_multiple(skip=skip, limit=page_size)
        total_pages = (total + page_size - 1) // page_size

        return PermissionListResponse(
            permissions=[PermissionResponse(**p.__dict__) for p in permissions],
            current_page=target_page,
            total_pages=total_pages,
            page_size=page_size,
        )

    async def delete(self, permission_id: int) -> bool:
        """
        Xóa permission.

        Args:
            permission_id (int): ID của permission cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        return await self._repository.delete(permission_id)
