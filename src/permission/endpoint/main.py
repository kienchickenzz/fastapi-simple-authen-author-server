"""
Router aggregation cho Permission module.
"""

from fastapi import APIRouter

from src.permission.endpoint.permission_endpoint import router as permission_router

main_router = APIRouter(prefix="/api")
main_router.include_router(permission_router)
