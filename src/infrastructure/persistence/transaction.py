import logging
from collections.abc import Callable
from contextvars import ContextVar
from functools import wraps
from typing import Any, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
logger = logging.getLogger(__name__)


current_session_context: ContextVar[AsyncSession | None] = ContextVar("current_session", default=None)


def set_current_session(session: AsyncSession) -> None:
    current_session_context.set(session)


def get_current_session() -> AsyncSession | None:
    return current_session_context.get()


def async_transactional(
    read_only: bool = False,
) -> Callable:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            session = get_current_session()

            needs_new_transaction = not session.in_transaction()
            try:
                if needs_new_transaction:
                    async with session.begin():
                        result = await func(self, *args, **kwargs)
                        if not read_only:
                            await session.commit()
                        await session.close()
                        return result
                else:
                    return await func(self, *args, **kwargs)

            except Exception:
                logger.exception("Transaction error")
                if session is not None and session.in_transaction():
                    await session.rollback()
                raise

        return cast(Callable[..., T], wrapper)

    return decorator
