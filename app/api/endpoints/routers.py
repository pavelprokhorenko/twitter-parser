from fastapi import APIRouter

from app.api.endpoints.twitter import tweets, user

api_router = APIRouter(prefix="/api")

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(tweets.router, prefix="/tweets", tags=["tweets"])
