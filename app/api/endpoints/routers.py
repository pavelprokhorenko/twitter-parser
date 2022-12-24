from fastapi import APIRouter

from app.api.endpoints.twitter import user

api_router = APIRouter(prefix="/api")

api_router.include_router(user.router, prefix="/user", tags=["user"])
