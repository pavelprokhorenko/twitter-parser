from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint

from app.db.base_class import Base


class ParseUserStatuses(Enum):
    FAILED = "FAILED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"


class User(Base):
    """
    Parsed user from Twitter.
    """

    __table_args__ = (
        # unique usernames among parse session
        UniqueConstraint("username", "session_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_id = Column(String(127))
    name = Column(String(127))
    username = Column(String(15), nullable=False, index=True)
    description = Column(String)
    following_count = Column(Integer)
    followers_count = Column(Integer)
    parse_status = Column(
        SAEnum(ParseUserStatuses, name="parse_user_statuses"),
        server_default=ParseUserStatuses.PENDING.name,
        nullable=False,
    )

    session_id = Column(
        ForeignKey("parsing_session.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
