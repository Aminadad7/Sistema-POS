from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.repositories.sale_repository import SaleRepository
from app.services.product_service import ProductService
from app.utils.constants import ITBIS_RATE
from app.utils.validators import require_text, require_positive_number
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SaleService:
    def __init__(self):
        self.repository = SaleRepository()
        self.product_service = ProductService()

    def calculate_totals(self, cart_items: list[dict], discount_percent: float = 0.0, apply_tax: bool = True) -> dict:
        subtotal = 0.0
        for item in cart_items:
            quantity = int(require_positive_number(item.get('quantity', 0), 'cantidad'))
            unit_price = require_positive_number(item.get('unit_price', 0.0), 'precio unitario')
            subtotal += unit_price * quantity

        discount_amount = subtotal * discount_percent
        subtotal_after_discount = subtotal - discount_amount
        tax = subtotal_after_discount * ITBIS_RATE if apply_tax else 0.0
        total = subtotal_after_discount + tax
        return {
            'subtotal': subtotal,
            'discount': discount_amount,
            'tax': tax,
            'total': total,
        }

    def create_sale(self, cashier: str, payment_method: str, cart_items: list[dict], discount_percent: float = 0.0, client_name: str | None = None, apply_tax: bool = True) -> Sale:
        cashier = require_text(cashier, 'cajero')
        payment_method = require_text(payment_method, 'método de pago')
        if not cart_items:
            raise ValueError('El carrito no puede estar vacío.')

        totals = self.calculate_totals(cart_items, discount_percent, apply_tax)
        sale = Sale(
            cashier=cashier,
            payment_method=payment_method,
            client_name=client_name.strip() if client_name else None,
            subtotal=totals['subtotal'],
            tax=totals['tax'],
            total=totals['total'],
        )

        for item in cart_items:
            quantity = int(require_positive_number(item.get('quantity', 0), 'cantidad'))
            unit_price = require_positive_number(item.get('unit_price', 0.0), 'precio unitario')
            product_name = require_text(item.get('product_name'), 'producto')
            product_id = item.get('product_id')

            sale_item = SaleItem(
                product_id=product_id,
                product_name=product_name,
                quantity=quantity,
                unit_price=unit_price,
                total_price=quantity * unit_price,
            )
            sale.items.append(sale_item)

            if product_id:
                try:
                    product = self.product_service.repository.get_by_id(product_id)
                    if product:
                        if product.stock < quantity:
                            raise ValueError(f'Stock insuficiente para {product.name}.')
                        product.stock -= quantity
                        self.product_service.repository.update(product)
                except Exception:
                    raise

        created_sale = self.repository.create_sale(sale)
        logger.info('Venta registrada: %s', created_sale)
        return created_sale
