"""
This module contains the user repository class
"""

from typing import Optional, Sequence

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from app.models.user import DBUser
from app.schemas.user import UserCreate, UserUpdate
from app.security import get_password_hash


class UserRepository:
    """
    This class contains the methods for the user repository
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def read(self, uid: int) -> Optional[DBUser]:
        """
        Retrieve a user by id

        :param uid:
        :return:
        """
        with Session(self.engine) as session:
            user = session.get(DBUser, uid)
            return user

    def read_by_username(self, username: str) -> Optional[DBUser]:
        """
        Retrieve a user by username

        :param username: the user username
        :return: the user
        :rtype: Optional[DBUser]
        """
        with Session(self.engine) as session:
            statement = select(DBUser).where(DBUser.username == username)
            user = session.exec(statement).first()
            return user

    def read_by_email(self, email: str) -> Optional[DBUser]:
        """
        Retrieve a user by email

        :param email: the user email
        :return: the user
        :rtype: Optional[DBUser]
        """
        with Session(self.engine) as session:
            statement = select(DBUser).where(DBUser.email == email)
            user = session.exec(statement).first()
            return user

    def read_all(self) -> Sequence[DBUser]:
        """
        Retrieve all users

        :return:
        """
        with Session(self.engine) as session:
            users = session.exec(select(DBUser)).all()
            return users

    def create(self, user_create: UserCreate) -> DBUser:
        """
        Create a new user

        :param user_create: the user data
        :return: the created user
        :rtype: DBUser
        """
        with Session(self.engine) as session:
            db_user = DBUser(**user_create.model_dump())
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

            return db_user

    def update(self, uid: int, user_update: UserUpdate) -> Optional[DBUser]:
        """
        Update a user

        :param uid: the user id
        :param user_update: the user data
        :return: the updated user
        :rtype: Optional[DBUser]
        """
        user_dict = user_update.model_dump()

        with Session(self.engine) as session:
            db_user = session.get(DBUser, uid)

            if not db_user:
                user_dict["hashed_password"] = get_password_hash(
                    user_dict.pop("password")
                )
                db_user = DBUser(id=uid, **user_dict)
                session.add(db_user)
            else:
                for key, value in user_dict.items():
                    if value is not None:
                        if hasattr(db_user, key):
                            setattr(db_user, key, value)
                        else:
                            # Handle fields that are not part of DBUser, e.g., password
                            if key == "password":
                                db_user.hashed_password = get_password_hash(value)

                session.add(db_user)

            session.commit()
            session.refresh(db_user)

            return db_user

    def delete(self, uid: int) -> bool:
        """
        Delete a user by id

        :param uid: the user id
        :return: True if the user was deleted, False otherwise
        :rtype: bool
        """
        with Session(self.engine) as session:
            user = session.get(DBUser, uid)

            if not user:
                return False

            session.delete(user)
            session.commit()
            return True
