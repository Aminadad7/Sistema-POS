from sqlalchemy.exc import IntegrityError
from app.database.session import SessionLocal
from app.models.client import Client
from app.repositories.base import BaseRepository


class ClientRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal())

    def _refresh_for_read(self) -> None:
        # Prevent stale SQLite reads from long-lived sessions.
        if self.session.in_transaction():
            self.session.rollback()
        self.session.expire_all()

    def get_by_id(self, client_id: int) -> Client | None:
        self._refresh_for_read()
        return self.session.get(Client, client_id)

    def list_all(self) -> list[Client]:
        self._refresh_for_read()
        return self.session.query(Client).order_by(Client.name).all()

    def add(self, client: Client) -> Client:
        self.session.add(client)
        try:
            self.commit()
        except IntegrityError:
            self.rollback()
            raise
        return client

    def update(self, client: Client) -> Client:
        try:
            self.commit()
        except IntegrityError:
            self.rollback()
            raise
        return client

    def delete(self, client: Client) -> None:
        self.session.delete(client)
        self.commit()
