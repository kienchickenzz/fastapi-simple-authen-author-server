"""
Entry point của FastAPI application.

Module này khởi tạo FastAPI app với các cấu hình:
- Load environment variables từ .env
- Setup AppInitializer để quản lý lifecycle
- Register tất cả routers từ các modules (health, ...)
- Cấu hình OpenAPI documentation với tags từ các modules
"""
from os import environ

from dotenv import load_dotenv

from src.base.app import create_fastapi_app
from src.config import Config
from src.initializer import AppInitializer
from src.auth.endpoint.main import main_router as router_auth
from src.auth.doc import Tags as AuthTags
from src.user.endpoint.main import main_router as router_user
from src.user.doc import Tags as UserTags
from src.permission.endpoint.main import main_router as router_permission
from src.permission.doc import Tags as PermissionTags
from src.role.endpoint.main import main_router as router_role
from src.role.doc import Tags as RoleTags


# Load environment variables
load_dotenv('.env')
config = Config(environ)

# Combine OpenAPI tags từ tất cả modules
openapi_tags = (
    AuthTags.get_docs()
    + UserTags.get_docs()
    + PermissionTags.get_docs()
    + RoleTags.get_docs()
)

# Khởi tạo FastAPI application
app = create_fastapi_app(
    config=config,
    initializer=AppInitializer,
    title="Simple Authorization",
    description="FastAPI with RBAC authorization system",
    version="0.1.0",
    team_name="core",
    team_url="https://invalid-address.ee",
    openapi_tags=openapi_tags,
)

# Register routers từ các modules
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_permission)
app.include_router(router_role)
