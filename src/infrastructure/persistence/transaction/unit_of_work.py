from __future__ import annotations

import abc
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Self, TypeVar, final

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from infrastructure.persistence.transaction.transaction import get_current_session

if TYPE_CHECKING:
    from types import TracebackType


EngineT = TypeVar("EngineT")


class UnitOfWorkError(Exception):
    """Base exception for unit of work errors"""

    pass


class AbstractUnitOfWork[EngineT](AbstractAsyncContextManager[Self], abc.ABC):
    """Abstract class for Unit of Work"""

    def __init__(self, engine: EngineT) -> None:
        self.engine = engine
        self.reuse_session: bool = False

    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        return self

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return None

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
        self._owns_session = False

    def __call__(self, *, reuse_session: bool = False):
        self.reuse_session = reuse_session
        return self

    async def __aenter__(self):
        context_session = get_current_session()

        if context_session is not None:
            self.session = context_session
            self._owns_session = False
        else:
            self.session = AsyncSession(self.engine)
            self._owns_session = True

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()

        # Only close if we own the session
        if self._owns_session:
            await self.close()

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
