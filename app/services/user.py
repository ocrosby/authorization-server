"""
This module contains the UserService class, which provides methods for user management.
"""

from typing import Optional, Sequence

from app.models.user import DBUser
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.security import get_password_hash


class UserService:
    """
    UserService class provides methods for user management.
    """

    def __init__(self, user_repository: UserRepository):
        self.repo = user_repository

    def create(self, user_create: UserCreate) -> DBUser:
        """
        Create a new user.

        :param user_create: The user data to create.
        :type user_create: UserCreate
        :return: The created user.
        :rtype: DBUser
        """
        hashed_password = get_password_hash(user_create.password)
        user_create.password = hashed_password
        return self.repo.create(user_create)

    def read(self, user_id: int) -> Optional[DBUser]:
        """
        Read a user by ID.

        :param user_id: The ID of the user to read.
        :type user_id: int
        :return: The user with the specified ID or None if not found.
        :rtype: Optional[DBUser]
        """
        return self.repo.read(user_id)

    def read_by_username(self, username: str) -> Optional[DBUser]:
        """
        Read a user by username.

        :param username: The username of the user to read.
        :type username: str
        :return: The user with the specified username or None if not found.
        :rtype: Optional[DBUser]
        """
        return self.repo.read_by_username(username)

    def read_by_email(self, email: str) -> Optional[DBUser]:
        """
        Read a user by email.

        :param email: The email of the user to read.
        :type email: str
        :return: The user with the specified email or None if not found.
        :rtype: Optional[DBUser]
        """
        return self.repo.read_by_email(email)

    def read_all(self) -> Sequence[DBUser]:
        """
        Retrieve all users

        :return: A list of all users.
        :rtype: Sequence[DBUser]
        """
        return self.repo.read_all()

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[DBUser]:
        """
        Update an existing user.

        :param user_id: The ID of the user to update.
        :type user_id: int
        :param user_data: The user data to update.
        :type user_data: UserUpdate
        :return: The updated user or None if the user was not found.
        :rtype: Optional[DBUser]
        """
        return self.repo.update(user_id, user_data)

    def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        :param user_id: The ID of the user to delete.
        :return: True if the user was deleted, False otherwise.
        :rtype: bool
        """
        return self.repo.delete(user_id)
