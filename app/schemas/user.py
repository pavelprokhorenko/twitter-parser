from pydantic import BaseModel


class TwitterUser(BaseModel):
    twitter_id: int
    name: str
    username: str
    following_count: int
    followers_count: int
    description: str
