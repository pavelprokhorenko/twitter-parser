from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.utils.sqlalchemy import to_snake_case_safe


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically.
        """
        obj_name = cls.__name__
        return to_snake_case_safe(obj_name)

    @classmethod
    @property
    def pk(cls) -> Any:
        """
        Primary Key of object (may not be assigned).
        """
        return cls.id
