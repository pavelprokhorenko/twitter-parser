from pydantic import BaseModel


class ParsingSession(BaseModel):
    session_id: int
