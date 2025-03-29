"""
This module contains the ClientService class, which provides methods for client management.
"""

from app.repositories.client import ClientRepository

from app.models.client import DBClient
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

    def read(self, client_id: int) -> DBClient:
        """
        Read a client by ID.

        :param client_id: The ID of the client to read.
        :return: The client with the specified ID.
        """
        return self.client_repository.get_by_id(client_id)

    def update(self, client_id: int, client_data: ClientUpdate) -> DBClient:
        """
        Update an existing client.

        :param client_id: The ID of the client to update.
        :param client_data: The new data for the client.
        :return: The updated client.
        """
        return self.client_repository.update(client_id, client_data)

    def delete(self, client_id: int) -> bool:
        """
        Delete a client by ID.

        :param client_id: The ID of the client to delete.
        :return: None
        """
        return self.client_repository.delete(client_id)
