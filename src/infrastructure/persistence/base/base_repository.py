from abc import ABC
from typing import Generic, TypeVar, final

from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.persistence.base.base_entities import Base

ModelT = TypeVar("ModelT", bound=Base)
SessionT = TypeVar("SessionT", bound=AsyncSession)


class AbstractRepository(ABC, Generic[SessionT]):
    """Abstract Repository wiith base for concrete implementation.

    Args:
        Generic (_type_): Type of table that you'll be using.

    """

    @final
    def __init__(self, session: SessionT) -> None:
        self.session = session


class SqlAlchemyRepository(AbstractRepository[AsyncSession], Generic[ModelT]):
    """SqlAlchemy Repository.

    Args:
        Generic (_type_): Type of table that you'll be using.

    """

    model: type[ModelT]

    @final
    def add(self, item: ModelT):
        self.session.add(item)

    @final
    def add_many(self, items: list[ModelT]):
        self.session.add_all(items)

    @final
    async def delete(self, item: ModelT):
        await self.session.delete(item)

    @final
    async def get_all_by_field(
        self, field: str, value: str | list[str], options: list | None = None
    ):
        if isinstance(value, list):
            query = (
                select(self.model)
                .where(getattr(self.model, field).in_(value))
                .order_by(self.model.created_at.desc())
            )
        else:
            query = (
                select(self.model)
                .where(getattr(self.model, field) == value)
                .order_by(self.model.created_at.desc())
            )
        if options:
            for option in options:
                query = query.options(option)
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    @final
    async def get_by_field(self, field: str, value: str, options: list | None = None):
        query = select(self.model).where(getattr(self.model, field) == value)
        if options:
            for option in options:
                query = query.options(option)
        result = await self.session.execute(query)
        return result.scalar()

    @final
    async def delete_by_field(self, field: str, value: str | int):
        query = delete(self.model).where(getattr(self.model, field) == value)
        await self.session.execute(query)

    @final
    async def delete_all_by_field(self, field: str, value: list[str | int]):
        query = delete(self.model).where(getattr(self.model, field).in_(value))
        await self.session.execute(query)

    @final
    async def get_all(self):
        query = select(self.model).order_by(self.model.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    @final
    async def update_by_field(self, field: str, value: str | int, data: dict):
        stmt = (
            update(self.model).where(getattr(self.model, field) == value).values(**data)
        )
        await self.session.execute(stmt)

    @final
    async def update_all_by_field(
        self, field: str, values: list[str | int], data: dict
    ):
        stmt = (
            update(self.model)
            .where(getattr(self.model, field).in_(values))
            .values(**data)
        )
        await self.session.execute(stmt)

    @final
    async def exists_by_field(self, field: str, value: str | int) -> bool:
        stmt = select(exists().where(getattr(self.model, field) == value))
        result = await self.session.execute(stmt)
        return result.scalar()
