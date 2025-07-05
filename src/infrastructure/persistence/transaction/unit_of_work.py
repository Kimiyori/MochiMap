from __future__ import annotations

import abc
from typing import TYPE_CHECKING, TypeVar, final

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.infrastructure.persistence.base.base_repository import SqlAlchemyRepository
from src.infrastructure.persistence.transaction.transaction import get_current_session, set_current_session

if TYPE_CHECKING:
    pass


EngineT = TypeVar("EngineT")


class UnitOfWorkError(Exception):
    """Base exception for unit of work errors"""

    pass


class AbstractUnitOfWork[EngineT]( abc.ABC):
    """Abstract class for Unit of Work"""

    def __init__(self, engine: EngineT) -> None:
        self.engine = engine


    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork[AsyncEngine]):
    """SqlAlchemy instance unit of work"""

    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine)
        self.session: AsyncSession | None = None
        self.repository: SqlAlchemyRepository|None= None
        context_session = get_current_session()

        if context_session is not None:
            self.session = context_session
        else:
            self.session = AsyncSession(self.engine)
            set_current_session(self.session)

    @final
    async def commit(self) -> None:
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.rollback()
            raise UnitOfWorkError(f"Failed to commit: {e}") from e

    @final
    async def flush(self) -> None:
        try:
            await self.session.flush()
        except SQLAlchemyError as e:
            await self.rollback()
            raise UnitOfWorkError(f"Failed to flush: {e}") from e

    @final
    async def rollback(self) -> None:
        try:
            await self.session.rollback()
        except SQLAlchemyError as e:
            raise UnitOfWorkError(f"Failed to rollback: {e}") from e

    @final
    async def close(self) -> None:
        await self.session.close()
