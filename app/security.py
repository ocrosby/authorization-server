# app/security.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    This function gets the password hash

    :param password:
    :return:
    """
    hashed_password: str = pwd_context.hash(password)
    return hashed_password
