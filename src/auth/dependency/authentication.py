"""
Dependency để xác thực user từ JWT token.
"""
import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.base.dependency_injection import Injects
from src.auth.dto.token_payload import TokenPayload
from src.auth.service.token_service import TokenService
from src.auth.database.repository.token_repository import TokenRepository
from src.auth.repository.permission_repository import PermissionRepository
from src.auth.exception.auth_exception import InvalidTokenException, ExpiredTokenException

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Injects("token_service"),
    token_repository: TokenRepository = Injects("token_repository"),
    permission_repository: PermissionRepository = Injects("permission_repository"),
) -> TokenPayload:
    """
    Dependency để lấy thông tin user hiện tại từ JWT token.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token từ header.
        token_service (TokenService): Service để decode JWT.
        token_repository (TokenRepository): Repository để check token status.
        permission_repository (PermissionRepository): Repository để query permissions.

    Returns:
        TokenPayload: Thông tin user bao gồm id và permissions.

    Raises:
        InvalidTokenException: Khi token không hợp lệ hoặc đã bị revoke.
        ExpiredTokenException: Khi token đã hết hạn.
    """
    token = credentials.credentials

    # Check token is active in database
    if not await token_repository.is_token_active(token):
        raise InvalidTokenException("Token is invalid or has been revoked")

    try:
        user_id = token_service.decode(token)
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()

    permissions = await permission_repository.get_permissions_by_user_id(user_id)

    return TokenPayload(user_id=user_id, permissions=permissions)
