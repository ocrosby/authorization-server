"""
This module contains the UserService class, which provides methods for user management.
"""

from typing import Sequence

from app.models.user import DBUser
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """
    UserService class provides methods for user management.
    """

    def __init__(self, user_repository: UserRepository):
        self.repo = user_repository

    def create(self, user_data: UserCreate) -> DBUser:
        """
        Create a new user.

        :param user_data:
        :return:
        """
        return self.repo.create(user_data)

    def read(self, user_id) -> DBUser:
        """
        Read a user by ID.

        :param user_id:
        :return:
        """
        return self.repo.read(user_id)

    def read_by_username(self, username: str) -> DBUser:
        """
        Read a user by username.

        :param username:
        :return:
        """
        return self.repo.read_by_username(username)

    def read_by_email(self, email: str) -> DBUser:
        """
        Read a user by email.

        :param email:
        :return:
        """
        return self.repo.read_by_email(email)

    def read_all(self) -> Sequence[DBUser]:
        """
        Retrieve all users

        :return: Sequence[DBUser]
        """
        return self.repo.read_all()

    def update(self, user_id: int, user_data: UserUpdate) -> DBUser:
        """
        Update an existing user.

        :param user_id:
        :param user_data:
        :return:
        """
        return self.repo.update(user_id, user_data)

    def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        :param user_id:
        :return:
        """
        return self.repo.delete(user_id)
