"""
This module contains the tasks for managing the project using Invoke.
"""

from invoke import task


@task(aliases=["i"])
def install(c):
    """Install the project dependencies."""
    c.run('pip install -e ".[dev]"')


@task(aliases=["r"])
def run(c):
    """Run the project."""
    c.run("uvicorn app.main:app --reload")


@task(aliases=["f"])
def format_code(c):
    """Format the source files using black."""
    c.run("black .")
