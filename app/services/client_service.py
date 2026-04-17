from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.utils.validators import require_text
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ClientService:
    def __init__(self):
        self.repository = ClientRepository()

    def list_clients(self) -> list[Client]:
        return self.repository.list_all()

    def create_client(self, name: str, email: str | None = None, phone: str | None = None, address: str | None = None) -> Client:
        client = Client(
            name=require_text(name, 'nombre'),
            email=email.strip() if email else None,
            phone=phone.strip() if phone else None,
            address=address.strip() if address else None,
        )
        saved = self.repository.add(client)
        logger.info('Cliente creado: %s', saved)
        return saved

    def update_client(self, client: Client, name: str, email: str | None = None, phone: str | None = None, address: str | None = None) -> Client:
        client.name = require_text(name, 'nombre')
        client.email = email.strip() if email else None
        client.phone = phone.strip() if phone else None
        client.address = address.strip() if address else None
        saved = self.repository.update(client)
        logger.info('Cliente actualizado: %s', saved)
        return saved

    def delete_client(self, client: Client):
        self.repository.delete(client)
        logger.info('Cliente eliminado: %s', client)
