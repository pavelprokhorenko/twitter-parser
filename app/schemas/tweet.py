from datetime import datetime

from pydantic import BaseModel


class Tweet(BaseModel):
    id: int
    text: str
    created_at: datetime
    lang: str
