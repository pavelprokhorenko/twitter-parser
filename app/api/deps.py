from collections.abc import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import async_session


async def get_db_pg() -> Generator[AsyncSession]:
    """
    Connect to database. After response disconnect from database.
    """
    async with async_session() as db:
        db: AsyncSession
        yield db
