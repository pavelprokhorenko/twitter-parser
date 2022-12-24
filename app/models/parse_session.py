from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from app.db.base_class import Base


class ParseSession(Base):
    """
    Session for parsing data from Twitter API.
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
