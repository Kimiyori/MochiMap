from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.common.error_handling import register_error_handling
from src.common.memory_monitor import MemoryMonitor
from src.core.routes import add_routes
from src.infrastructure.dependencies.app_container import AppContainer
from src.infrastructure.persistence.mapper import start_mapper
from src.modules.roadmap.use_cases import roadmap_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.memory_monitor.start()
    db = app.state.container.infrastructure.db()
    await db.connect()
    start_mapper()

    yield

    await db.disconnect()
    await app.state.memory_monitor.stop()


def create_app() -> FastAPI:
    """Factory for creating a FastAPI client."""
    container = AppContainer()
    app = FastAPI(
        title="MochiMap API",
        version="0.0.1",
        root_path="/api",
        redirect_slashes=False,
        lifespan=lifespan,
    )
    app.state.container = container
    app.state.memory_monitor = MemoryMonitor(
        threshold_percent=30,
        check_interval_seconds=60,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SessionMiddleware, secret_key="some-random-string")  # noqa: S106

    add_routes([roadmap_router], app)

    register_error_handling(app)

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run("main:create_app", host="127.0.0.1", port=8000, reload=True, factory=True)
