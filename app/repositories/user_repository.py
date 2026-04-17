from sqlalchemy.exc import IntegrityError
from app.database.session import SessionLocal
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal())

    def find_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.query(User).get(user_id)

    def create(self, username: str, password_hash: bytes, role: str) -> User:
        user = User(username=username, password_hash=password_hash, role=role)
        self.session.add(user)
        try:
            self.commit()
        except IntegrityError:
            self.rollback()
            raise
        return user

    def update(self, user: User, role: str | None = None, password_hash: bytes | None = None) -> User:
        if role:
            user.role = role
        if password_hash:
            user.password_hash = password_hash
        self.session.add(user)
        self.commit()
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.commit()

    def count_admins(self) -> int:
        return self.session.query(User).filter(User.role == 'admin').count()

    def list_users(self) -> list[User]:
        return self.session.query(User).order_by(User.username).all()
