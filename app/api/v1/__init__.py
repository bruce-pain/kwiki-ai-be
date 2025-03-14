from fastapi import APIRouter

from app.api.v1.auth.routes import auth

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(router=auth)
