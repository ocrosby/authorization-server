"""
This module contains the tasks for managing the project using Invoke.
"""

import re
import sys
from typing import Dict, Optional

from invoke import Context, task


@task(aliases=["c"])
def clean(c: Context):
    """Clean the project by removing __pycache__ directories and .pyc files."""
    c.run("find app -type d -name '__pycache__' -exec rm -rf {} +")
    c.run("find app -type f -name '*.pyc' -delete")

    c.run("find tests -type d -name htmlcov -exec rm -rf {} +")
    c.run("find tests -type f -name coverage.xml -delete")
    c.run("find tests -type f -name junit.xml -delete")
    c.run("find tests -type f -name .coverage -delete")

    c.run("rm -f coverage.xml junit.xml .coverage")
    c.run("rm -rf htmlcov")


@task(
    pre=[clean],
    aliases=["i"],
    help={"prod": "Install production dependencies."},
)
def install(c: Context, prod: bool = False):
    """Install dependencies."""
    c.run('pip install --upgrade "pip>=21.3"')
    c.run("pip install flit")
    c.run("pip install build")

    if prod:
        print("Installing production dependencies ...")
        c.run("flit install --deps production")
    else:
        print("Installing development dependencies...")
        c.run("flit install --symlink")  # install package in editable mode


@task(aliases=["n"])
def install_node(c: Context):
    """Install the Node.js dependencies."""
    print("Installing Node.js dependencies...")
    c.run("npm install")
    c.run("npm install --save-dev @commitlint/{config-conventional,cli}")


@task(aliases=["r"])
def run(c: Context):
    """Run the project."""
    c.run("uvicorn app.main:app --reload")


@task(aliases=["f"])
def format_code(c: Context):
    """Format the source files using black."""
    print("Formatting code with black and isort...")
    c.run("black app/ tests/ tasks.py update_version.py")
    c.run("isort app/ tests/ tasks.py update_version.py")
    print("Code formatted successfully.")


@task(aliases=["l"], pre=[format_code])
def lint(c: Context):
    """Lint the source files using flake8."""
    print("Linting source files...")
    print("Running pylint...")
    c.run("pylint app/")
    print("Running flake8...")
    c.run("flake8 app/")
    print("Running mypy...")
    c.run("mypy app/")
    print("Linting completed.")


@task(aliases=["cl"])
def commitlint(c: Context):
    """Check the most recent commit message against commitlint."""
    print("Running commitlint...")
    c.run("git log -1 --pretty=%B | npx commitlint")


@task(aliases=["t"])
def test(c: Context):
    """Run the tests using pytest."""
    c.run("pytest --disable-warnings -v tests/unit/")


@task(aliases=["v"])
def coverage(c):
    """Runs PyTest unit and integration tests with coverage."""
    c.run("coverage run -m pytest tests/unit")
    c.run("coverage lcov -o ./coverage/lcov.info")


@task(aliases=["cc"])
def check_complexity(c: Context, max_complexity: int = 12) -> None:
    """
    Check the cyclomatic complexity of the code.
    Fail if it exceeds the max_complexity.

    :param c: The context instance (automatically passed by invoke).
    :param max_complexity: The maximum allowed cyclomatic complexity.
    """
    c.run("echo 'Checking cyclomatic complexity ...'")
    c.run(f"cyclo -m {max_complexity} .")
