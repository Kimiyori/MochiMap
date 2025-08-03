"""Command line argument parsing for the test runner."""

import argparse


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Comprehensive test runner for MochiMap backend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py --only-unit       # Run only unit tests
  python run_tests.py --only-integration # Run only integration tests
  python run_tests.py -v --tb=short     # Run all tests with verbose output and short traceback
  python run_tests.py --only-unit -k "test_user"  # Run only unit tests matching "test_user"
        """,
    )

    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument("--only-unit", action="store_true", help="Run only unit tests")
    test_group.add_argument("--only-integration", action="store_true", help="Run only integration tests")

    # Parse known args to separate our flags from pytest args
    known_args, unknown_args = parser.parse_known_args()

    # Add unknown args as pytest args
    known_args.pytest_args = unknown_args

    return known_args
