from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class SaleItem(Base):
    __tablename__ = 'sale_items'

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product_name = Column(String(120), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False, default=0.0)

    sale = relationship('Sale', back_populates='items')
    product = relationship('Product', back_populates='sale_items')

    def __repr__(self):
        return f'<SaleItem(product={self.product_name}, quantity={self.quantity})>'
