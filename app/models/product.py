from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    sku = Column(String(60), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False, default=0.0)
    stock = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    category = relationship('Category', back_populates='products')
    sale_items = relationship('SaleItem', back_populates='product')

    def __repr__(self):
        return f'<Product(name={self.name}, sku={self.sku}, price={self.price})>'
