#!/usr/bin/env python3
"""
Comprehensive test runner for MochiMap backend.

This script can run unit tests, integration tests, or both with parallel execution.
For integration tests, it automatically manages the database lifecycle.
"""

import sys

from run_script import (
    parse_arguments,
    run_all_tests,
    run_integration_tests,
    run_unit_tests,
)


def main() -> None:
    """Main entry point for the test runner."""
    args = parse_arguments()

    exit_code = 0

    if args.only_unit:
        exit_code = run_unit_tests(args.pytest_args)
    elif args.only_integration:
        exit_code = run_integration_tests(args.pytest_args)
    else:
        exit_code = run_all_tests(args.pytest_args)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
