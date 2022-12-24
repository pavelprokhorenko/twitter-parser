from fastapi import APIRouter

from app.api.endpoints.twitter import users

api_router = APIRouter(prefix="/api")

api_router.include_router(users.router, prefix="/users", tags=["users"])
