from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

from .base import CRUDBase


class CRUDUser(CRUDBase[User]):
    """
    CRUD operations for Twitter user.
    """

    async def get(self, db: AsyncSession, *, pk: str) -> User | None:
        return await super().get(db, pk=pk)

    async def get_all(
        self, db: AsyncSession, session_id: int | None = None
    ) -> list[User]:
        query = select(self._model)
        if session_id:
            query = query.where(self._model.session_id == session_id)

        result = await db.execute(query)
        return result.scalars().all()

    async def create(
        self, db: AsyncSession, *, obj_in: BaseModel | dict[str, Any]
    ) -> User:
        return await super().create(db, obj_in=obj_in)

    async def update(
        self, db: AsyncSession, *, pk: str, obj_in: BaseModel | dict[str, Any]
    ) -> User:
        return await super().update(db, pk=pk, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, pk: str) -> None:
        return await super().delete(db, pk=pk)


user = CRUDUser(User)
