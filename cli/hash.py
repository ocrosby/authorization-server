"""
This script hashes a given password from the command line
"""

import click

from app.utils import get_password_hash


@click.command()
@click.argument("password")
def hash_password(password):
    """
    This function hashes the given password

    :param password: The password to hash
    """
    hashed_password = get_password_hash(password)
    print(f"Hashed password: {hashed_password}")
