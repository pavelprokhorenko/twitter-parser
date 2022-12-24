from typing import Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parsing_session import ParsingSession

from .base import CRUDBase


class CRUDParsingSession(CRUDBase[ParsingSession]):
    """
    CRUD operations for Parsing Session.
    """

    async def get(self, db: AsyncSession, *, pk: int) -> ParsingSession | None:
        return await super().get(db, pk=pk)

    async def get_all(self, db: AsyncSession) -> list[ParsingSession]:
        return await super().get_all(db)

    async def create(
        self, db: AsyncSession, *, obj_in: BaseModel | dict[str, Any]
    ) -> ParsingSession:
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: AsyncSession, *, pk: Any, obj_in: BaseModel | dict[str, Any]
    ) -> ParsingSession:
        return await super().update(db, pk=pk, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: Any) -> None:
        return await super().delete(db, pk=pk)


parsing_session = CRUDParsingSession(ParsingSession)
