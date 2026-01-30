#!/usr/bin/env python3
"""
Install dlt packages with automatic dependency manager detection.

This script detects the current dependency manager (uv, pip, poetry, pipenv)
and installs the required dlt packages based on the destination and features.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional


def detect_dependency_manager() -> Optional[str]:
    """
    Detect the dependency manager used in the current project.

    Returns:
        The dependency manager name ('uv', 'poetry', 'pipenv', 'pip') or None
    """
    # Check for uv
    if Path("uv.lock").exists() or Path("pyproject.toml").exists():
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            return "uv"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Check for poetry
    if Path("poetry.lock").exists() or (Path("pyproject.toml").exists() and "tool.poetry" in Path("pyproject.toml").read_text()):
        try:
            subprocess.run(["poetry", "--version"], capture_output=True, check=True)
            return "poetry"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Check for pipenv
    if Path("Pipfile").exists():
        try:
            subprocess.run(["pipenv", "--version"], capture_output=True, check=True)
            return "pipenv"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Check for pip (always available in Python environments)
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, check=True)
        return "pip"
    except subprocess.CalledProcessError:
        pass

    return None


def ask_user_for_manager() -> str:
    """
    Ask user which dependency manager to use.

    Returns:
        The chosen dependency manager name
    """
    print("\nNo dependency manager detected. Which would you like to use?")
    print("1. uv (recommended - fast, modern)")
    print("2. pip (standard)")
    print("3. poetry")
    print("4. pipenv")

    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        if choice == "1":
            return "uv"
        elif choice == "2":
            return "pip"
        elif choice == "3":
            return "poetry"
        elif choice == "4":
            return "pipenv"
        else:
            print("Invalid choice. Please enter 1-4.")


def ensure_uv_project_initialized() -> None:
    """
    Ensure the project is initialized for uv by checking for pyproject.toml.
    If not present, runs 'uv init' to create it.
    """
    if not Path("pyproject.toml").exists():
        print("No pyproject.toml found. Initializing project with 'uv init'...")
        try:
            subprocess.run(["uv", "init"], check=True)
            print("✅ Project initialized with uv")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize project: {e}", file=sys.stderr)
            sys.exit(1)


def install_packages(manager: str, packages: list[str]) -> None:
    """
    Install packages using the specified dependency manager.

    Args:
        manager: The dependency manager to use
        packages: List of package specifications to install
    """
    print(f"\nInstalling packages using {manager}:")
    print(f"  {' '.join(packages)}")

    if manager == "uv":
        ensure_uv_project_initialized()
        cmd = ["uv", "add"] + packages
    elif manager == "pip":
        cmd = [sys.executable, "-m", "pip", "install"] + packages
    elif manager == "poetry":
        cmd = ["poetry", "add"] + packages
    elif manager == "pipenv":
        cmd = ["pipenv", "install"] + packages
    else:
        raise ValueError(f"Unknown dependency manager: {manager}")

    try:
        subprocess.run(cmd, check=True)
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}", file=sys.stderr)
        sys.exit(1)


def get_required_packages(destination: Optional[str] = None, include_workspace: bool = True) -> list[str]:
    """
    Get the list of packages to install based on destination and features.

    Args:
        destination: The dlt destination (e.g., 'bigquery', 'snowflake', 'duckdb')
        include_workspace: Whether to include dlt[workspace] for dashboard support

    Returns:
        List of package specifications
    """
    # Build combined extras list for a single dlt package
    extras = []

    # Add destination extra (duckdb is included by default, so skip it)
    if destination and destination != "duckdb":
        extras.append(destination)

    # Add workspace support for dashboard/pipeline show command
    if include_workspace:
        extras.append("workspace")

    # Return single package with combined extras, or base dlt if no extras
    if extras:
        return [f"dlt[{','.join(extras)}]"]
    else:
        return ["dlt"]


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Install dlt packages with automatic dependency manager detection"
    )
    parser.add_argument(
        "--destination",
        help="The dlt destination (e.g., bigquery, snowflake, duckdb, postgres)",
        default=None
    )
    parser.add_argument(
        "--no-workspace",
        help="Don't install workspace support (dashboard/show command)",
        action="store_true"
    )
    parser.add_argument(
        "--manager",
        help="Force a specific dependency manager (uv, pip, poetry, pipenv)",
        choices=["uv", "pip", "poetry", "pipenv"],
        default=None
    )

    args = parser.parse_args()

    # Detect or ask for dependency manager
    if args.manager:
        manager = args.manager
        print(f"Using specified dependency manager: {manager}")
    else:
        manager = detect_dependency_manager()
        if manager:
            print(f"Detected dependency manager: {manager}")
        else:
            manager = ask_user_for_manager()

    # Get required packages
    packages = get_required_packages(
        destination=args.destination,
        include_workspace=not args.no_workspace
    )

    # Install packages
    install_packages(manager, packages)


if __name__ == "__main__":
    main()
