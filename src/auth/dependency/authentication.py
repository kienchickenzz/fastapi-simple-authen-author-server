"""
Dependency để xác thực user từ JWT token.

Token đã chứa đầy đủ thông tin (user_id, username, permissions),
không cần query database để lấy permissions.
"""
import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.base.dependency_injection import Injects
from src.auth.dto.token_payload import TokenPayload
from src.auth.service.token_service import TokenService
from src.auth.database.repository.token_repository import TokenRepository
from src.auth.exception.auth_exception import InvalidTokenException, ExpiredTokenException

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Injects("token_service"),
    token_repository: TokenRepository = Injects("token_repository"),
) -> TokenPayload:
    """
    Dependency để lấy thông tin user hiện tại từ JWT token.

    Token đã chứa permissions, không cần query database.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token từ header.
        token_service (TokenService): Service để decode JWT.
        token_repository (TokenRepository): Repository để check token status.

    Returns:
        TokenPayload: Thông tin user bao gồm id, username và permissions.

    Raises:
        InvalidTokenException: Khi token không hợp lệ hoặc đã bị revoke.
        ExpiredTokenException: Khi token đã hết hạn.
    """
    token = credentials.credentials

    # Check token is active in database (để hỗ trợ revoke)
    if not await token_repository.is_token_active(token):
        raise InvalidTokenException("Token is invalid or has been revoked")

    try:
        # Decode token trả về TokenPayload với permissions đã có sẵn
        payload = token_service.decode(token)
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()

    return payload
