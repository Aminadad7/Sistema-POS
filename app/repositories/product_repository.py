from sqlalchemy.exc import IntegrityError
from app.database.session import SessionLocal
from app.models.product import Product
from app.models.category import Category
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal())

    def _refresh_for_read(self) -> None:
        # End any long-lived read transaction so SQLite returns current data.
        if self.session.in_transaction():
            self.session.rollback()
        self.session.expire_all()

    def get_by_id(self, product_id: int) -> Product | None:
        self._refresh_for_read()
        return self.session.get(Product, product_id)

    def find_by_sku(self, sku: str) -> Product | None:
        self._refresh_for_read()
        return self.session.query(Product).filter(Product.sku == sku).first()

    def list_all(self) -> list[Product]:
        self._refresh_for_read()
        return self.session.query(Product).order_by(Product.name).all()

    def list_categories(self) -> list[Category]:
        self._refresh_for_read()
        return self.session.query(Category).order_by(Category.name).all()

    def add(self, product: Product) -> Product:
        self.session.add(product)
        try:
            self.commit()
        except IntegrityError:
            self.rollback()
            raise
        return product

    def update(self, product: Product) -> Product:
        try:
            self.commit()
        except IntegrityError:
            self.rollback()
            raise
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.commit()
