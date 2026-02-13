"""
Endpoints cho Permission CRUD operations.
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.base.dependency_injection import Injects
from src.auth.dto.token_payload import TokenPayload
from src.auth.dependency.authorization import require_permissions
from src.permission.dto.permission_dto import (
    PermissionCreateRequest,
    PermissionListRequest,
)
from src.permission.service.permission_service import PermissionService
from src.permission.doc import Tags

router = APIRouter(tags=[Tags.PERMISSION], prefix="/permissions")


@router.post(
    path="",
    summary="Create Permission",
    description="Create a new permission",
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    request: PermissionCreateRequest,
    _: TokenPayload = Depends(require_permissions("permission:create")),
    permission_service: PermissionService = Injects("permission_service"),
) -> JSONResponse:
    """
    Tạo permission mới.

    Args:
        request (PermissionCreateRequest): Thông tin permission cần tạo.
        _ (TokenPayload): Token payload (cần permission permission:create).
        permission_service (PermissionService): Service xử lý permission.

    Returns:
        JSONResponse: Permission đã tạo.
    """
    result = await permission_service.create(request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=201)


@router.get(
    path="",
    summary="List Permissions",
    description="Get paginated list of permissions",
    status_code=status.HTTP_200_OK,
)
async def list_permissions(
    request: PermissionListRequest = Depends(PermissionListRequest.as_query),
    _: TokenPayload = Depends(require_permissions("permission:read")),
    permission_service: PermissionService = Injects("permission_service"),
) -> JSONResponse:
    """
    Lấy danh sách permissions với phân trang.

    Args:
        request (PermissionListRequest): Request với thông tin phân trang.
        _ (TokenPayload): Token payload (cần permission permission:read).
        permission_service (PermissionService): Service xử lý permission.

    Returns:
        JSONResponse: Danh sách permissions.
    """
    result = await permission_service.get_list(request.target_page, request.page_size)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.delete(
    path="/{permission_id}",
    summary="Delete Permission",
    description="Delete permission by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_permission(
    permission_id: int,
    _: TokenPayload = Depends(require_permissions("permission:delete")),
    permission_service: PermissionService = Injects("permission_service"),
) -> None:
    """
    Xóa permission theo ID.

    Args:
        permission_id (int): ID của permission cần xóa.
        _ (TokenPayload): Token payload (cần permission permission:delete).
        permission_service (PermissionService): Service xử lý permission.
    """
    await permission_service.delete(permission_id)
    return None
