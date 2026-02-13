"""
Endpoints cho Role CRUD operations.
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.base.dependency_injection import Injects
from src.auth.dto.token_payload import TokenPayload
from src.auth.dependency.authorization import require_permissions
from src.role.dto.role_dto import (
    RoleCreateRequest,
    RoleUpdateRequest,
    RoleListRequest,
    RolePermissionAssignRequest,
)
from src.role.service.role_service import RoleService
from src.role.doc import Tags

router = APIRouter(tags=[Tags.ROLE], prefix="/roles")


@router.post(
    path="",
    summary="Create Role",
    description="Create a new role",
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    request: RoleCreateRequest,
    _: TokenPayload = Depends(require_permissions("role:create")),
    role_service: RoleService = Injects("role_service"),
) -> JSONResponse:
    """
    Tạo role mới.

    Args:
        request (RoleCreateRequest): Thông tin role cần tạo.
        _ (TokenPayload): Token payload (cần permission role:create).
        role_service (RoleService): Service xử lý role.

    Returns:
        JSONResponse: Role đã tạo.
    """
    result = await role_service.create(request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=201)


@router.get(
    path="",
    summary="List Roles",
    description="Get paginated list of roles",
    status_code=status.HTTP_200_OK,
)
async def list_roles(
    request: RoleListRequest = Depends(RoleListRequest.as_query),
    _: TokenPayload = Depends(require_permissions("role:read")),
    role_service: RoleService = Injects("role_service"),
) -> JSONResponse:
    """
    Lấy danh sách roles với phân trang.

    Args:
        request (RoleListRequest): Request với thông tin phân trang.
        _ (TokenPayload): Token payload (cần permission role:read).
        role_service (RoleService): Service xử lý role.

    Returns:
        JSONResponse: Danh sách roles.
    """
    result = await role_service.get_list(request.target_page, request.page_size)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.get(
    path="/{role_id}",
    summary="Get Role",
    description="Get role by ID with permissions",
    status_code=status.HTTP_200_OK,
)
async def get_role(
    role_id: int,
    _: TokenPayload = Depends(require_permissions("role:read")),
    role_service: RoleService = Injects("role_service"),
) -> JSONResponse:
    """
    Lấy thông tin một role theo ID (bao gồm permissions).

    Args:
        role_id (int): ID của role.
        _ (TokenPayload): Token payload (cần permission role:read).
        role_service (RoleService): Service xử lý role.

    Returns:
        JSONResponse: Thông tin role với permissions.
    """
    result = await role_service.get_one(role_id)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.put(
    path="/{role_id}",
    summary="Update Role",
    description="Update role by ID",
    status_code=status.HTTP_200_OK,
)
async def update_role(
    role_id: int,
    request: RoleUpdateRequest,
    _: TokenPayload = Depends(require_permissions("role:update")),
    role_service: RoleService = Injects("role_service"),
) -> JSONResponse:
    """
    Cập nhật thông tin role.

    Args:
        role_id (int): ID của role cần update.
        request (RoleUpdateRequest): Thông tin cần update.
        _ (TokenPayload): Token payload (cần permission role:update).
        role_service (RoleService): Service xử lý role.

    Returns:
        JSONResponse: Role đã update.
    """
    result = await role_service.update(role_id, request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.delete(
    path="/{role_id}",
    summary="Delete Role",
    description="Delete role by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_role(
    role_id: int,
    _: TokenPayload = Depends(require_permissions("role:delete")),
    role_service: RoleService = Injects("role_service"),
) -> None:
    """
    Xóa role theo ID.

    Args:
        role_id (int): ID của role cần xóa.
        _ (TokenPayload): Token payload (cần permission role:delete).
        role_service (RoleService): Service xử lý role.
    """
    await role_service.delete(role_id)
    return None


# === Role-Permission endpoints ===

@router.get(
    path="/{role_id}/permissions",
    summary="Get Role Permissions",
    description="Get all permissions assigned to a role",
    status_code=status.HTTP_200_OK,
)
async def get_role_permissions(
    role_id: int,
    _: TokenPayload = Depends(require_permissions("role:read")),
    role_service: RoleService = Injects("role_service"),
) -> JSONResponse:
    """
    Lấy danh sách permissions của role.

    Args:
        role_id (int): ID của role.
        _ (TokenPayload): Token payload (cần permission role:read).
        role_service (RoleService): Service xử lý role.

    Returns:
        JSONResponse: Danh sách permissions của role.
    """
    result = await role_service.get_permissions(role_id)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.post(
    path="/{role_id}/permissions",
    summary="Assign Permission to Role",
    description="Assign a permission to a role",
    status_code=status.HTTP_201_CREATED,
)
async def assign_permission_to_role(
    role_id: int,
    request: RolePermissionAssignRequest,
    _: TokenPayload = Depends(require_permissions("role:update")),
    role_service: RoleService = Injects("role_service"),
) -> JSONResponse:
    """
    Gán permission cho role.

    Args:
        role_id (int): ID của role.
        request (RolePermissionAssignRequest): Request chứa permission_id.
        _ (TokenPayload): Token payload (cần permission role:update).
        role_service (RoleService): Service xử lý role.

    Returns:
        JSONResponse: Thông báo thành công.
    """
    await role_service.assign_permission(role_id, request.permission_id)
    return JSONResponse(
        content={"message": "Permission assigned successfully"},
        status_code=201,
    )


@router.delete(
    path="/{role_id}/permissions/{permission_id}",
    summary="Remove Permission from Role",
    description="Remove a permission from a role",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    _: TokenPayload = Depends(require_permissions("role:update")),
    role_service: RoleService = Injects("role_service"),
) -> None:
    """
    Xóa permission khỏi role.

    Args:
        role_id (int): ID của role.
        permission_id (int): ID của permission cần xóa.
        _ (TokenPayload): Token payload (cần permission role:update).
        role_service (RoleService): Service xử lý role.
    """
    await role_service.remove_permission(role_id, permission_id)
    return None
