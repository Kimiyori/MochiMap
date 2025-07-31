from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.core.routes import add_routes
from src.dependencies.container import Container
from src.infrastructure.persistence.mapper import start_mapper
from src.modules.roadmap.use_cases import roadmap_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = app.container.infrastructure.db()
    await db.connect()
    start_mapper()

    yield

    # clear_mappers()
    await db.disconnect()


def create_app() -> FastAPI:
    """Factory for creating a FastAPI client."""
    container = Container()
    app = FastAPI(
        title="MochiMap API",
        version="0.0.1",
        root_path="/api",
        redirect_slashes=False,
        lifespan=lifespan,
    )
    app.container = container
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SessionMiddleware, secret_key="some-random-string")  # noqa: S106

    add_routes([roadmap_router], app)
    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run("main:create_app", host="127.0.0.1", port=8000, reload=True, factory=True)
