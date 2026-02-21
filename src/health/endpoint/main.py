"""
Module tổng hợp các routers của Health module.
Đăng ký tất cả endpoints với prefix /api.
"""
from fastapi import APIRouter

from src.health.endpoint.endpoint_health import router as router_health

main_router = APIRouter(prefix="/api")
main_router.include_router(router_health)
