from pydantic import BaseModel

from app.models.user import ParseUserStatuses


class TwitterUser(BaseModel):
    twitter_id: str
    name: str
    username: str
    following_count: int
    followers_count: int
    description: str


class ParseUsers(BaseModel):
    username: str
    status: ParseUserStatuses
