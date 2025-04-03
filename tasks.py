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


@task(aliases=["l"])
def lint(c: Context):
    """Lint the source files using flake8."""
    print("Linting source files...")
    print("Running pylint...")
    c.run("pylint app/")
    print("Running flake8...")
    c.run("flake8 app/")
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
    result = c.run("radon cc app -s", hide=True)

    if result is None:
        print("No output from radon.")
        sys.exit(1)

    output = result.stdout
    results = parse_radon_output(output)
    display_radon_results(results)
    max_score = get_max_score(results)

    if max_score > max_complexity:
        print(
            f"\nFAILED - Maximum complexity {max_complexity} exceeded by {max_score}\n"
        )

        print("\nFunctions with complexity greater than the maximum allowed:")
        display_exceeded_complexity(results, max_complexity)

        sys.exit(1)

    print(f"\nMaximum complexity not exceeded: {max_score}\n")

    sys.exit(0)


def get_max_score(results: Dict[Optional[str], any]) -> int:
    max_score = 0
    for _, functions in results.items():
        for function in functions:
            if function["score"] > max_score:
                max_score = function["score"]
    return max_score


def display_exceeded_complexity(
    results: Dict[Optional[str], any], max_complexity: int
) -> None:
    print("File\tFunction\tComplexity\tScore")
    for file, functions in results.items():
        for function in functions:
            if function["score"] > max_complexity:
                print(
                    f"{file}\t{function['name']}\t{function['complexity']}\t{function['score']}"
                )


def display_radon_results(results: Dict[Optional[str], any]) -> None:
    for file, functions in results.items():
        print(f"\nFile: {file}")
        for function in functions:
            print(
                f"\tFunction: {function['name']}, ",
                f"Complexity: {function['complexity']}, ",
                f"Score: {function['score']}",
            )


def parse_radon_output(output: str) -> Dict[Optional[str], any]:
    # Remove the escape sequence
    output = output.replace("\x1b[0m", "")

    # Regular expression to match the lines with complexity information
    pattern = re.compile(r"^\s*(\w)\s(\d+:\d+)\s([\w_]+)\s-\s([A-F])\s\((\d+)\)$")

    # Dictionary to store the results
    results: Dict[Optional[str], any] = {}

    # Split the output into lines
    output = output.strip()
    lines = output.splitlines()

    current_file = None
    for line in lines:
        try:
            # Check if the line is a file name
            if not line.startswith(" "):
                current_file = line.strip()
                results[current_file] = []
            else:
                # Match the line with the pattern
                match = pattern.match(line)
                if match:
                    function_info = {
                        "type": match.group(1),
                        "location": match.group(2),
                        "name": match.group(3),
                        "complexity": match.group(4),
                        "score": int(match.group(5)),
                    }
                    results[current_file].append(function_info)
        except ValueError as e:
            print(f"Error parsing line: '{line}'")
            print(e)

    return results
