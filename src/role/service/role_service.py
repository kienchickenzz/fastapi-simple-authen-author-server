"""
Service xử lý business logic cho Role.
"""

from src.role.database.repository.role_repository import RoleRepository
from src.role.database.repository.role_permission_repository import RolePermissionRepository
from src.permission.database.repository.permission_repository import PermissionRepository
from src.permission.dto.permission_dto import PermissionResponse
from src.role.dto.role_dto import (
    RoleCreateRequest,
    RoleUpdateRequest,
    RoleResponse,
    RoleDetailResponse,
    RoleListResponse,
    RolePermissionsResponse,
)


class RoleService:
    """
    Service cho Role operations.

    Args:
        role_repository (RoleRepository): Repository để truy cập roles.
        role_permission_repository (RolePermissionRepository): Repository để quản lý role-permission.
        permission_repository (PermissionRepository): Repository để truy cập permissions.
    """

    def __init__(
        self,
        role_repository: RoleRepository,
        role_permission_repository: RolePermissionRepository,
        permission_repository: PermissionRepository,
    ):
        """
        Khởi tạo RoleService.

        Args:
            role_repository (RoleRepository): Repository để truy cập roles.
            role_permission_repository (RolePermissionRepository): Repository junction table.
            permission_repository (PermissionRepository): Repository để truy cập permissions.
        """
        self._role_repository = role_repository
        self._role_permission_repository = role_permission_repository
        self._permission_repository = permission_repository

    async def create(self, request: RoleCreateRequest) -> RoleResponse:
        """
        Tạo role mới.

        Args:
            request (RoleCreateRequest): Thông tin role cần tạo.

        Returns:
            RoleResponse: Role đã tạo.
        """
        values = {
            "name": request.name,
            "description": request.description,
        }
        role = await self._role_repository.create(values)
        return RoleResponse(**role.__dict__)

    async def get_one(self, role_id: int) -> RoleDetailResponse:
        """
        Lấy thông tin một role với danh sách permissions.

        Args:
            role_id (int): ID của role.

        Returns:
            RoleDetailResponse: Thông tin role với permissions.
        """
        role = await self._role_repository.get_one(role_id)
        if not role:
            raise ValueError(f"Role with id {role_id} not found")

        permissions = await self._role_permission_repository.get_permissions_by_role_id(role_id)
        permission_responses = [PermissionResponse(**p.__dict__) for p in permissions]

        return RoleDetailResponse(
            **role.__dict__,
            permissions=permission_responses,
        )

    async def get_list(self, target_page: int, page_size: int) -> RoleListResponse:
        """
        Lấy danh sách roles với phân trang.

        Args:
            target_page (int): Trang cần lấy.
            page_size (int): Số lượng mỗi trang.

        Returns:
            RoleListResponse: Danh sách roles.
        """
        skip = (target_page - 1) * page_size
        roles, total = await self._role_repository.get_multiple(skip=skip, limit=page_size)
        total_pages = (total + page_size - 1) // page_size

        return RoleListResponse(
            roles=[RoleResponse(**r.__dict__) for r in roles],
            current_page=target_page,
            total_pages=total_pages,
            page_size=page_size,
        )

    async def update(self, role_id: int, request: RoleUpdateRequest) -> RoleResponse:
        """
        Cập nhật thông tin role.

        Args:
            role_id (int): ID của role cần update.
            request (RoleUpdateRequest): Thông tin cần update.

        Returns:
            RoleResponse: Role đã update.
        """
        values = request.model_dump(exclude_unset=True)
        role = await self._role_repository.update(role_id, values)
        if not role:
            raise ValueError(f"Role with id {role_id} not found")
        return RoleResponse(**role.__dict__)

    async def delete(self, role_id: int) -> bool:
        """
        Xóa role.

        Args:
            role_id (int): ID của role cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        return await self._role_repository.delete(role_id)

    # === Role-Permission operations ===

    async def get_permissions(self, role_id: int) -> RolePermissionsResponse:
        """
        Lấy danh sách permissions của role.

        Args:
            role_id (int): ID của role.

        Returns:
            RolePermissionsResponse: Danh sách permissions.
        """
        permissions = await self._role_permission_repository.get_permissions_by_role_id(role_id)
        permission_responses = [PermissionResponse(**p.__dict__) for p in permissions]

        return RolePermissionsResponse(
            role_id=role_id,
            permissions=permission_responses,
        )

    async def assign_permission(self, role_id: int, permission_id: int) -> None:
        """
        Gán permission cho role.

        Args:
            role_id (int): ID của role.
            permission_id (int): ID của permission.

        Raises:
            ValueError: Nếu role hoặc permission không tồn tại,
                       hoặc đã được gán trước đó.
        """
        # Kiểm tra role tồn tại
        role = await self._role_repository.get_one(role_id)
        if not role:
            raise ValueError(f"Role with id {role_id} not found")

        # Kiểm tra permission tồn tại
        permission = await self._permission_repository.get_one(permission_id)
        if not permission:
            raise ValueError(f"Permission with id {permission_id} not found")

        # Kiểm tra đã gán chưa
        if await self._role_permission_repository.has_permission(role_id, permission_id):
            raise ValueError(f"Permission already assigned to role")

        await self._role_permission_repository.assign_permission(role_id, permission_id)

    async def remove_permission(self, role_id: int, permission_id: int) -> None:
        """
        Xóa permission khỏi role.

        Args:
            role_id (int): ID của role.
            permission_id (int): ID của permission.

        Raises:
            ValueError: Nếu không tìm thấy assignment.
        """
        success = await self._role_permission_repository.remove_permission(role_id, permission_id)
        if not success:
            raise ValueError(f"Permission {permission_id} not assigned to role {role_id}")
