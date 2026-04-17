from sqlalchemy import Column, Integer, String
from app.database.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False)

    def __repr__(self):
        return f'<User(username={self.username}, role={self.role})>'
