"""
This module contains the client repository class
"""

from typing import Optional, Sequence

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from app.models.client import DBClient
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository:
    """
    This class contains the methods for the client repository
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def read(self, uid: int) -> Optional[DBClient]:
        """
        Retrieve a client by id

        :param uid:
        :return:
        """
        with Session(self.engine) as session:
            client = session.get(DBClient, uid)
            return client

    def read_all(self) -> Sequence[DBClient]:
        """
        Retrieve all clients

        :return:
        """
        with Session(self.engine) as session:
            clients = session.exec(select(DBClient)).all()
            return clients

    def create(self, client: ClientCreate) -> DBClient:
        """
        Create a new client

        :param client: the client data
        :return: the created client
        :rtype: DBClient
        """
        db_client = DBClient(**client.model_dump())
        with Session(self.engine) as session:
            session.add(db_client)
            session.commit()
            session.refresh(db_client)

            return db_client

    def update(self, uid: int, client: ClientUpdate) -> Optional[DBClient]:
        """
        Update a client

        :param uid: the client id
        :param client: the client data
        :return: the updated client
        :rtype: Optional[DBClient]
        """
        client_dict = client.model_dump()

        with Session(self.engine) as session:
            db_client = session.get(DBClient, uid)

            if not db_client:
                db_client = DBClient(id=uid, **client_dict)
                session.add(db_client)
            else:
                for key, value in client_dict.items():
                    if value is not None:
                        setattr(db_client, key, value)

                session.add(db_client)

            session.commit()
            session.refresh(db_client)

            return db_client

    def delete(self, uid: int) -> bool:
        """
        Delete a client by id

        :param uid: the client id
        :return: True if the client was deleted, False otherwise
        :rtype: bool
        """
        with Session(self.engine) as session:
            client = session.get(DBClient, uid)

            if not client:
                return False

            session.delete(client)
            session.commit()
            return True
