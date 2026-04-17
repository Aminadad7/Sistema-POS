from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)

    def __repr__(self):
        return f'<Client(name={self.name}, email={self.email})>'
