import os
from pathlib import Path

from fastapi import FastAPI


def add_routes(routes, app: FastAPI):
    for route in routes:
        if route:
            app.include_router(route)


def discover_api_modules(base_path: Path):
    package_root = base_path.parent  # Go up one level to include 'src' in the path
    api_paths = base_path.rglob("modules/**/api.py")

    modules = []
    for path in api_paths:
        rel_path = os.path.relpath(path, package_root)
        module_path = rel_path.replace(os.sep, ".").replace(".py", "")
        modules.append(module_path)

    return modules
