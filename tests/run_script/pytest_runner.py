"""Pytest execution utilities with argument validation and parallel support."""

import subprocess


def run_pytest(test_path: str, additional_args: list[str], parallel: bool = True) -> int:

    safe_args = []
    for arg in additional_args:
        # Allow pytest-style arguments (starting with -, containing alphanumeric, =, /, \, :, .)
        if arg.startswith("-") or all(c.isalnum() or c in "=/\\:._-" for c in arg):
            safe_args.append(arg)
        else:
            print(f"Warning: Skipping potentially unsafe argument: {arg}")

    base_command = ["pytest"]
    if parallel:
        base_command.extend(["-n", "auto"])
    base_command.append(test_path)
    command = base_command + safe_args

    print(f"Running: {' '.join(command)}")

    try:
        result = subprocess.run(command, check=False)  # noqa: S603
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        return 130
    else:
        return result.returncode
