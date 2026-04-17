from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, nullable=False)
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category(name={self.name})>'
