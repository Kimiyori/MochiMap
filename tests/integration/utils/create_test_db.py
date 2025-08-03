import os

import docker


def set_test_env():
    os.environ["POSTGRES_USER"] = "user"
    os.environ["POSTGRES_PASSWORD"] = "password"  # noqa: S105
    os.environ["POSTGRES_DB"] = "test_db"
    os.environ["POSTGRES_PORT"] = "54329"
    os.environ["POSTGRES_HOST"] = "localhost"


def run_db_container():
    client = docker.from_env()
    return client.containers.run(
        image="postgres:16-alpine",
        name="postgres_complex_test",
        detach=True,
        environment={
            "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
            "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "PGDATA": "/var/lib/postgresql/data",
            "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
        },
        remove=True,
        ports={"5432/tcp": os.environ.get("POSTGRES_PORT")},
        healthcheck={
            "test": ["CMD", "pg_isready", "-d", os.environ.get("POSTGRES_DB"), "-U", os.environ.get("POSTGRES_USER")],
            "interval": 1000000000,  # 1 second in nanoseconds
            "timeout": 1000000000,  # 1 second in nanoseconds
            "retries": 10,
        },
    )



def get_container_status(container_name):
    client = docker.from_env()
    return client.api.inspect_container(container_name)["State"]["Health"]["Status"]


def get_db_uri():
    return (
        f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
        f"@localhost:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
    )
