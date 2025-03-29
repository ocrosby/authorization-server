"""
This module contains the UserService class, which provides methods for user management.
"""

from app.schemas.user import UserCreate, UserUpdate
from app.models.user import DBUser


class UserService:
    """
    UserService class provides methods for user management.
    """

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create(self, user_data: UserCreate) -> DBUser:
        """
        Create a new user.

        :param user_data:
        :return:
        """
        return self.user_repository.create_user(user_data)

    def read(self, user_id) -> DBUser:
        """
        Read a user by ID.

        :param user_id:
        :return:
        """
        return self.user_repository.get_user(user_id)

    def update(self, user_id: int, user_data: UserUpdate) -> DBUser:
        """
        Update an existing user.

        :param user_id:
        :param user_data:
        :return:
        """
        return self.user_repository.update_user(user_id, user_data)

    def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        :param user_id:
        :return:
        """
        return self.user_repository.delete_user(user_id)
