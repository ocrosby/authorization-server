"""
This module contains the ClientService class, which provides methods for client management.
"""

from typing import Optional, Sequence

from app.models.client import DBClient
from app.repositories.client import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    """
    This class is the client service
    """

    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def create(self, client_data: ClientCreate) -> DBClient:
        """
        Create a new client.

        :param client_data: The data for the new client.
        :return: The created client.
        """
        return self.client_repository.create(client_data)

    def read(self, client_id: int) -> Optional[DBClient]:
        """
        Read a client by ID.

        :param client_id: The ID of the client to read.
        :type client_id: int
        :return: The client with the specified ID.
        :rtype: Optional[DBClient]
        """
        return self.client_repository.read(client_id)

    def read_all(self) -> Sequence[DBClient]:
        """
        Retrieve all clients.

        :return: A list of all clients.
        :rtype: Sequence[DBClient]
        """
        return self.client_repository.read_all()

    def update(self, client_id: int, client_data: ClientUpdate) -> Optional[DBClient]:
        """
        Update an existing client.

        :param client_id: The ID of the client to update.
        :type client_id: int
        :param client_data: The new data for the client.
        :type client_data: ClientUpdate
        :return: The updated client.
        :rtype: DBClient
        """
        return self.client_repository.update(client_id, client_data)

    def delete(self, client_id: int) -> bool:
        """
        Delete a client by ID.

        :param client_id: The ID of the client to delete.
        :type client_id: int
        :return: True if the client was deleted, False otherwise.
        :rtype: bool
        """
        return self.client_repository.delete(client_id)
