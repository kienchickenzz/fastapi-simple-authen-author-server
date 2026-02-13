"""
Router aggregation cho Role module.
"""

from fastapi import APIRouter

from src.role.endpoint.role_endpoint import router as role_router

main_router = APIRouter(prefix="/api")
main_router.include_router(role_router)
