import random

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.utils.validators import require_text, require_positive_number
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def list_products(self) -> list[Product]:
        return self.repository.list_all()

    def list_categories(self):
        return self.repository.list_categories()

    def _generate_sku(self, name: str) -> str:
        base = ''.join(word[0].upper() for word in name.split() if word)[:4]
        base = base.ljust(2, 'X')
        sku = None
        attempts = 0
        while attempts < 10:
            suffix = f'{random.randint(1000, 9999)}'
            candidate = f'{base}{suffix}'
            if not self.repository.find_by_sku(candidate):
                sku = candidate
                break
            attempts += 1
        if sku is None:
            raise ValueError('No se pudo generar un SKU único para el producto.')
        return sku

    def create_product(self, name: str, price: float, stock: int, category_id: int | None):
        validated_name = require_text(name, 'nombre')
        sku = self._generate_sku(validated_name)
        product = Product(
            name=validated_name,
            sku=sku,
            price=require_positive_number(price, 'precio'),
            stock=int(require_positive_number(stock, 'stock')),
            category_id=category_id,
        )
        saved = self.repository.add(product)
        logger.info('Producto creado: %s', saved)
        return saved

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.repository.get_by_id(product_id)

    def update_product(self, product_id: int, name: str, price: float, stock: int, category_id: int | None):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError('Producto no encontrado.')
        product.name = require_text(name, 'nombre')
        product.price = require_positive_number(price, 'precio')
        product.stock = int(require_positive_number(stock, 'stock'))
        product.category_id = category_id
        saved = self.repository.update(product)
        logger.info('Producto actualizado: %s', saved)
        return saved

    def delete_product(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError('Producto no encontrado.')
        self.repository.delete(product)
        logger.info('Producto eliminado: %s', product)
