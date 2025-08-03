"""Test execution strategies for different test types."""

import sys

from .database_manager import start_db, stop_db
from .pytest_runner import run_pytest


def run_unit_tests(additional_args: list[str]) -> int:
    """Run unit tests."""
    print("=== Running Unit Tests ===")
    return run_pytest("tests/unit", additional_args, parallel=True)


def run_integration_tests(additional_args: list[str]) -> int:
    """Run integration tests with database lifecycle management."""
    print("=== Running Integration Tests ===")

    # Start database
    try:
        start_db()
    except Exception as e:
        print(f"Failed to start database: {e}", file=sys.stderr)
        return 1

    # Run tests
    exit_code = 0
    try:
        exit_code = run_pytest("tests/integration", additional_args, parallel=True)
    except Exception as e:
        print(f"Error running integration tests: {e}", file=sys.stderr)
        exit_code = 1
    finally:
        # Always stop the database, regardless of test outcome
        try:
            stop_db()
        except Exception as e:
            print(f"Error during cleanup: {e}", file=sys.stderr)
            if exit_code == 0:
                exit_code = 1

    return exit_code


def run_all_tests(additional_args: list[str]) -> int:
    """Run both unit and integration tests."""
    print("=== Running All Tests ===")

    # Run unit tests first (faster, no DB required)
    unit_exit_code = run_unit_tests(additional_args)

    # Run integration tests
    integration_exit_code = run_integration_tests(additional_args)

    # Return non-zero if any test suite failed
    if unit_exit_code != 0:
        print(f"Unit tests failed with exit code: {unit_exit_code}")
    if integration_exit_code != 0:
        print(f"Integration tests failed with exit code: {integration_exit_code}")

    return unit_exit_code or integration_exit_code
