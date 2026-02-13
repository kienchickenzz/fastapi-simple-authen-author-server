from os import environ

from dotenv import load_dotenv

from src.base.app import create_fastapi_app
from src.config import Config
from src.initializer import AppInitializer
from src.health.endpoint.main import main_router as router_health
from src.health.doc import Tags as HealthTags
from src.auth.endpoint.main import main_router as router_auth
from src.auth.doc import Tags as AuthTags
from src.user.endpoint.main import main_router as router_user
from src.user.doc import Tags as UserTags
from src.book.endpoint.main import main_router as router_book
from src.book.doc import Tags as BookTags
from src.permission.endpoint.main import main_router as router_permission
from src.permission.doc import Tags as PermissionTags
from src.role.endpoint.main import main_router as router_role
from src.role.doc import Tags as RoleTags

load_dotenv('.env')
config = Config(environ)

# Combine all OpenAPI tags
openapi_tags = (
    HealthTags.get_docs()
    + AuthTags.get_docs()
    + UserTags.get_docs()
    + BookTags.get_docs()
    + PermissionTags.get_docs()
    + RoleTags.get_docs()
)

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

# Service routes
app.include_router(router_health)
app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_book)
app.include_router(router_permission)
app.include_router(router_role)
