import asyncio
import contextlib
import time
from collections.abc import AsyncGenerator

import nest_asyncio
import pytest
from dependency_injector.providers import Singleton
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command
from alembic.config import Config
from main import create_app
from src.infrastructure.persistence.connection.connection import AsyncDatabase
from tests.integration.utils.config import get_container_status, get_db_uri, run_db_container, set_test_env

nest_asyncio.apply()

app = create_app()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _database():
    set_test_env()
    container = run_db_container()
    container_status = "starting"
    while container_status not in {"healthy", "unhealthy"}:
        time.sleep(1)
        container_status = get_container_status(container.name)

    if container_status == "unhealthy":
        container.stop()
        pytest.exit("Test DB container not started")

    yield

    container.stop()


@pytest.fixture(scope="session")
async def _migrations(_database):
    alembic_conf = Config("alembic.ini")
    command.upgrade(alembic_conf, "head")


@pytest.fixture(scope="session", autouse=True)
async def db_override(_migrations):
    app.container.infrastructure.db.override(Singleton(AsyncDatabase, get_db_uri()))
    db = app.container.infrastructure.db()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()


@pytest.fixture()
async def session(db_override) -> AsyncGenerator[AsyncSession]:
    session = AsyncSession(bind=db_override.engine, expire_on_commit=False)

    # Track objects created during the test
    created_objects = []
    original_add = session.add

    # Override add method to track objects
    def tracking_add(obj):
        created_objects.append(obj)
        return original_add(obj)

    # Replace session.add with our tracking version
    session.add = tracking_add

    try:
        yield session
    finally:
        # Delete only objects created during this test
        for obj in created_objects:
            with contextlib.suppress(Exception):
                await session.delete(obj)
        await session.commit()
        await session.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient]:
    import httpx

    # Use the transport approach for async testing
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        yield client
