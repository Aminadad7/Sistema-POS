from datetime import datetime, timedelta
from collections import defaultdict
from calendar import month_name
from app.repositories.sale_repository import SaleRepository
from app.utils.logger import get_logger
from app.utils.settings_manager import get_setting

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

    def product_sales_summary(self, limit: int = 5):
        sales = self.repository.list_all()
        product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
        for sale in sales:
            for item in sale.items:
                product_data[item.product_name]['quantity'] += item.quantity
                product_data[item.product_name]['revenue'] += item.total_price

        sorted_products = sorted(
            product_data.items(),
            key=lambda kv: kv[1]['quantity'],
            reverse=True,
        )
        return [
            (product_name, data['quantity'], data['revenue'])
            for product_name, data in sorted_products[:limit]
        ]

    def client_sales_summary(self, limit: int = 5):
        sales = self.repository.list_all()
        client_data = defaultdict(lambda: {'count': 0, 'total': 0.0})
        for sale in sales:
            client_name = sale.client_name or 'Consumidor Final'
            client_data[client_name]['count'] += 1
            client_data[client_name]['total'] += sale.total

        sorted_clients = sorted(
            client_data.items(),
            key=lambda kv: kv[1]['count'],
            reverse=True,
        )
        return [
            (client_name, data['count'], data['total'])
            for client_name, data in sorted_clients[:limit]
        ]

    def monthly_sales_summary(self, months: int = 6):
        sales = self.repository.list_all()
        monthly_data = defaultdict(lambda: {'total': 0.0, 'count': 0})
        for sale in sales:
            year = sale.created_at.year
            month = sale.created_at.month
            key = (year, month)
            monthly_data[key]['total'] += sale.total
            monthly_data[key]['count'] += 1

        now = datetime.utcnow()
        result = []
        for index in range(months - 1, -1, -1):
            month_year = (now.year, now.month - index)
            year = month_year[0]
            month = month_year[1]
            while month <= 0:
                month += 12
                year -= 1
            key = (year, month)
            data = monthly_data.get(key, {'total': 0.0, 'count': 0})
            result.append((f'{month_name[month]} {year}', data['total'], data['count']))

        return result

    def list_all_sales(self):
        logger.info('Listando todas las ventas')
        return self.repository.list_all()

    def get_sale_by_id(self, sale_id: int):
        return self.repository.get_by_id(sale_id)

    def build_invoice_data_from_sale(self, sale):
        if sale is None:
            raise ValueError('Venta no encontrada.')

        return {
            'invoice_number': f'FAC{sale.id:06d}',
            'date': sale.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'business_name': get_setting('business_name') or 'Mi Negocio',
            'business_address': get_setting('business_address') or '',
            'business_phone': get_setting('business_phone') or '',
            'business_logo_path': get_setting('business_logo_path') or '',
            'client_name': sale.client_name or 'Consumidor Final',
            'cashier': sale.cashier,
            'payment_method': sale.payment_method,
            'discount_percent': 0.0,
            'subtotal': sale.subtotal,
            'discount': max(0.0, sale.subtotal + sale.tax - sale.total),
            'tax': sale.tax,
            'tax_applied': sale.tax > 0,
            'total': sale.total,
            'paid_amount': sale.total,
            'change_amount': 0.0,
            'items': [
                {
                    'name': item.product_name,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'total_price': item.total_price,
                }
                for item in sale.items
            ],
        }

    def top_products(self, limit: int = 10):
        return self.repository.top_products(limit)
