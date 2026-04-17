from datetime import datetime, timedelta
from app.repositories.sale_repository import SaleRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReportService:
    def __init__(self):
        self.repository = SaleRepository()

    def sales_today(self):
        now = datetime.utcnow()
        start = datetime(now.year, now.month, now.day)
        end = start + timedelta(days=1)
        logger.info('Generando reporte de ventas del día')
        return self.repository.list_by_period(start, end)

    def sales_for_month(self, year: int, month: int):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        logger.info('Generando reporte de ventas para %s-%s', year, month)
        return self.repository.list_by_period(start, end)

    def sales_summary_by_period(self, start: datetime, end: datetime):
        sales = self.repository.list_by_period(start, end)
        total_sales = sum(sale.total for sale in sales)
        total_tax = sum(sale.tax for sale in sales)
        total_discounts = sum(max(0.0, sale.subtotal + sale.tax - sale.total) for sale in sales)
        return {
            'sales': sales,
            'count': len(sales),
            'total_sales': total_sales,
            'total_tax': total_tax,
            'total_discounts': total_discounts,
        }

    def sales_today_summary(self):
        now = datetime.utcnow()
        start = datetime(now.year, now.month, now.day)
        end = start + timedelta(days=1)
        logger.info('Generando resumen de ventas del día')
        return self.sales_summary_by_period(start, end)

    def sales_for_month_summary(self, year: int, month: int):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)
        logger.info('Generando resumen de ventas para %s-%s', year, month)
        return self.sales_summary_by_period(start, end)

    def top_products(self, limit: int = 10):
        return self.repository.top_products(limit)
