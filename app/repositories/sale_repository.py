from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.database.session import SessionLocal
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.repositories.base import BaseRepository


class SaleRepository(BaseRepository):
    def __init__(self):
        super().__init__(SessionLocal())

    def create_sale(self, sale: Sale) -> Sale:
        self.session.add(sale)
        try:
            self.commit()
        except IntegrityError:
            self.rollback()
            raise
        return sale

    def list_by_period(self, start_date, end_date) -> list[Sale]:
        return self.session.query(Sale).filter(Sale.created_at >= start_date, Sale.created_at <= end_date).order_by(Sale.created_at.desc()).all()

    def top_products(self, limit: int = 10) -> list[tuple[str, int]]:
        return (
            self.session.query(SaleItem.product_name, func.sum(SaleItem.quantity).label('total'))
            .group_by(SaleItem.product_name)
            .order_by(func.sum(SaleItem.quantity).desc())
            .limit(limit)
            .all()
        )
