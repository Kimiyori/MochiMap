"""Database lifecycle management for integration tests."""

import sys
import time

from integration.utils.create_test_db import (
    get_container_status,
    run_db_container,
    set_test_env,
)

from alembic import command
from alembic.config import Config


def start_db() -> None:
    """Start the test database container and run migrations."""
    print("Starting test database...")
    set_test_env()
    container = run_db_container()
    container_status = "starting"

    while container_status not in {"healthy", "unhealthy"}:
        time.sleep(1)
        container_status = get_container_status(container.name)

    if container_status == "unhealthy":
        container.stop()
        print("Test DB container failed to start", file=sys.stderr)
        sys.exit(1)

    print("Test DB container started successfully.")

    # Run migrations
    alembic_conf = Config("alembic.ini")
    command.upgrade(alembic_conf, "head")
    print("Database migrations applied.")


def stop_db() -> None:
    """Stop the test database container."""
    from docker import from_env

    client = from_env()
    try:
        container = client.containers.get("postgres_complex_test")
        container.stop()
        print("Test DB container stopped.")
    except Exception as e:
        print(f"Error stopping container: {e}", file=sys.stderr)
