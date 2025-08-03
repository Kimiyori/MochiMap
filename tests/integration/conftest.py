import asyncio
import uuid
from collections.abc import AsyncGenerator, Callable

import httpx
import nest_asyncio
import pytest
from dependency_injector.providers import Singleton
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.engine import AsyncDatabase
from src.infrastructure.persistence.mapper import start_mapper
from src.infrastructure.persistence.transaction import set_current_session
from tests.integration.utils.create_test_app import create_test_app
from tests.integration.utils.create_test_db import get_db_uri, set_test_env
from tests.integration.utils.transaction_manager import test_transaction_manager

nest_asyncio.apply()
app = create_test_app()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def db_override():
    set_test_env()
    app.container.infrastructure.db.override(Singleton(AsyncDatabase, get_db_uri()))
    db = app.container.infrastructure.db()
    await db.connect()
    start_mapper()
    try:
        yield db
    finally:
        await db.disconnect()


@pytest.fixture(scope="session")
async def base_client() -> AsyncGenerator[AsyncClient]:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture()
async def transactional_session(db_override) -> AsyncGenerator[tuple[AsyncSession, str]]:
    session = AsyncSession(bind=db_override.engine, expire_on_commit=False)

    transaction = await session.begin()

    transaction_token = str(uuid.uuid4())
    test_transaction_manager.create_transaction(transaction_token, session)

    set_current_session(session)

    try:
        yield session, transaction_token
    finally:
        if transaction.is_active:
            await transaction.rollback()

        test_transaction_manager.remove_transaction(transaction_token)
        await session.close()


@pytest.fixture()
async def trans_token(transactional_session) -> AsyncGenerator[str]:
    _, token = transactional_session
    yield token


@pytest.fixture()
async def session(transactional_session) -> AsyncGenerator[AsyncSession]:
    session, _ = transactional_session
    yield session


@pytest.fixture
async def client(base_client: AsyncClient, trans_token: str) -> AsyncGenerator[AsyncClient]:
    def wrap_method(method: Callable) -> Callable:
        async def wrapped(*args, **kwargs):
            headers = kwargs.pop("headers", {}) or {}
            headers["x-transaction-token"] = trans_token
            kwargs["headers"] = headers
            return await method(*args, **kwargs)

        return wrapped

    for method_name in ("get", "post", "put", "patch", "delete"):
        orig = getattr(base_client, method_name)
        setattr(base_client, method_name, wrap_method(orig))

    yield base_client
