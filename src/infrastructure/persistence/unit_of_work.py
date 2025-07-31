from __future__ import annotations

from typing import final

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.infrastructure.persistence.base.base_repository import ModelT, SqlAlchemyRepository
from src.infrastructure.persistence.transaction import get_current_session, set_current_session


class UnitOfWorkError(Exception):
    """Base exception for unit of work errors"""

    def __init__(self, error: str):
        super().__init__(f"Unit of Work Error: {error}")


class SqlAlchemyUnitOfWork[ModelT]:
    """SqlAlchemy instance unit of work"""

    def __init__(self, engine: AsyncEngine, repository_cls: type[SqlAlchemyRepository[ModelT]]) -> None:
        self.session: AsyncSession | None = None
        context_session = get_current_session()

        if context_session is not None:
            self.session = context_session
        else:
            self.session = AsyncSession(engine)
            set_current_session(self.session)

        self.repository = repository_cls(self.session)

    @final
    async def commit(self) -> None:
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.rollback()
            raise UnitOfWorkError(str(e)) from e

    @final
    async def flush(self) -> None:
        try:
            await self.session.flush()
        except SQLAlchemyError as e:
            await self.rollback()
            raise UnitOfWorkError(str(e)) from e

    @final
    async def rollback(self) -> None:
        try:
            await self.session.rollback()
        except SQLAlchemyError as e:
            raise UnitOfWorkError(str(e)) from e

    @final
    async def close(self) -> None:
        await self.session.close()
