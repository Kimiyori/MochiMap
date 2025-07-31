from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.pool import NullPool


class AsyncDatabase:
    def __init__(self, db_uri: str) -> None:
        self._db_uri = db_uri
        self._engine: AsyncEngine | None = None

    async def connect(self):
        self._engine = create_async_engine(
            self._db_uri, echo=False, pool_pre_ping=True, poolclass=NullPool
        )

    async def disconnect(self):
        await self._engine.dispose()

    @property
    def engine(self):
        return self._engine
