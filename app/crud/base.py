from typing import Any, Generic, Optional, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    """
    CRUD object with async default methods to Create, Read, Update, Delete (CRUD) database objects.
    """

    def __init__(self, model: type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, *, pk: Any) -> Optional[ModelType]:
        query = select(self._model).where(self._model.pk == pk)
        result = await db.execute(query)

        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> list[ModelType]:
        query = select(self._model)
        result = await db.execute(query)

        return result.scalars().all()

    async def create(
        self, db: AsyncSession, *, obj_in: Union[BaseModel, dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(exclude_unset=True)

        query = insert(self._model).values(**obj_in_data).returning(self._model)

        result = await db.execute(query)
        await db.commit()

        return result.mappings().first()

    async def update(
        self, db: AsyncSession, *, pk: Any, obj_in: Union[BaseModel, dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        query = (
            update(self._model)
            .values(**update_data)
            .where(self._model.pk == pk)
            .returning(self._model)
        )

        result = await db.execute(query)
        await db.commit()

        return result.mappings().first()

    async def delete(self, db: AsyncSession, *, pk: Any) -> None:
        query = delete(self._model).where(self._model.pk == pk)

        await db.execute(query)
        await db.commit()
