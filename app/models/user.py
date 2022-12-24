from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class User(Base):
    """
    Parsed user from Twitter.
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(127), nullable=False)
    username = Column(String(15), unique=True, nullable=False, index=True)
    description = Column(String)
    following_count = Column(Integer, server_default="0", nullable=False)
    followers_count = Column(Integer, server_default="0", nullable=False)
