from datetime import datetime
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QMessageBox,
    QSpinBox,
    QDoubleSpinBox,
    QAbstractItemView,
    QCheckBox,
    QSizePolicy,
    QHeaderView,
)
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from app.repositories.product_repository import ProductRepository
from app.services.client_service import ClientService
from app.services.sale_service import SaleService
from app.utils.constants import ITBIS_RATE
from app.utils.pdf_generator import generate_invoice_pdf
from app.utils.settings_manager import get_setting


class SalesView(QWidget):
    sale_completed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_repository = ProductRepository()
        self.sale_service = SaleService()
        self.current_user = None
        self.cart_items: list[dict] = []
        self.selected_product_id = None
        self.current_invoice_number = None
        self.current_invoice_path = None
        self.updating_cart_table = False
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Registro de Ventas')
        self.title_label.setObjectName('titleLabel')

        self.product_search_input = QLineEdit()
        self.product_search_input.setPlaceholderText('Buscar producto por nombre o SKU')
        self.product_search_input.textChanged.connect(self.filter_products)

        self.client_selector = QComboBox()
        self.client_selector.addItem('Cliente no seleccionado', None)
        self.client_selector.currentIndexChanged.connect(self.on_client_selected)

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText('Nombre del cliente (opcional, Consumidor Final si no se ingresa)')

        self.apply_tax_checkbox = QCheckBox('Aplicar ITBIS')

        self.client_service = ClientService()
        self.selected_invoice_client_id = None
        self.apply_tax_checkbox.setChecked(True)
        self.apply_tax_checkbox.stateChanged.connect(self.update_totals)

        self.payment_method_input = QComboBox()
        self.payment_method_input.addItems(['Efectivo', 'Tarjeta'])

        self.payment_amount_input = QDoubleSpinBox()
        self.payment_amount_input.setPrefix('RD$ ')
        self.payment_amount_input.setDecimals(2)
        self.payment_amount_input.setMinimum(0.00)
        self.payment_amount_input.setMaximum(9999999.99)
        self.payment_amount_input.valueChanged.connect(self.update_change)

        self.change_label = QLabel('Cambio: 0.00')
        self.change_label.setStyleSheet('font-size: 14pt; font-weight: bold;')

        self.add_button = QPushButton('Agregar al carrito')
        self.add_button.clicked.connect(self.add_to_cart)
        self.remove_button = QPushButton('Quitar selección')
        self.remove_button.clicked.connect(self.remove_from_cart)
        self.checkout_button = QPushButton('Finalizar venta')
        self.checkout_button.clicked.connect(self.finalize_sale)
        self.export_pdf_button = QPushButton('Generar factura PDF')
        self.export_pdf_button.clicked.connect(self.export_invoice_pdf)
        self.export_pdf_button.setEnabled(False)
        self.view_invoice_button = QPushButton('Ver / Imprimir factura')
        self.view_invoice_button.clicked.connect(self.open_invoice_file)
        self.view_invoice_button.setEnabled(False)

        self.product_table = QTableWidget(0, 6)
        self.product_table.setHorizontalHeaderLabels(['ID', 'Nombre', 'SKU', 'Precio', 'Stock', 'Categoría'])
        self.product_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.product_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.product_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.product_table.setMinimumHeight(280)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.verticalHeader().setVisible(False)
        self.product_table.setAlternatingRowColors(True)
        self.product_table.itemSelectionChanged.connect(self.load_product_selection)
        self.product_table.itemDoubleClicked.connect(self.add_product_by_double_click)

        self.cart_table = QTableWidget(0, 4)
        self.cart_table.setHorizontalHeaderLabels(['Producto', 'Cantidad', 'Precio', 'Total'])
        self.cart_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.cart_table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked | QTableWidget.EditKeyPressed)
        self.cart_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cart_table.setMinimumHeight(260)
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.itemChanged.connect(self.on_cart_item_changed)

        self.discount_input = QSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setSuffix(' %')
        self.discount_input.setValue(0)
        self.discount_input.valueChanged.connect(self.update_totals)

        self.subtotal_label = QLabel('Subtotal: 0.00')
        self.discount_label = QLabel('Descuento: 0.00')
        self.tax_label = QLabel(f'ITBIS ({int(ITBIS_RATE*100)}%): 0.00')
        self.total_label = QLabel('Total: 0.00')

        for label in [self.subtotal_label, self.discount_label, self.tax_label, self.total_label]:
            label.setStyleSheet('font-size: 16pt; font-weight: bold;')

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.product_search_input)
        left_layout.addWidget(self.product_table)
        left_layout.addWidget(QLabel('Cliente registrado:'))
        left_layout.addWidget(self.client_selector)
        left_layout.addWidget(QLabel('Nombre del cliente:'))
        left_layout.addWidget(self.client_name_input)
        left_layout.addWidget(self.apply_tax_checkbox)
        left_layout.addWidget(QLabel('Método de pago:'))
        left_layout.addWidget(self.payment_method_input)
        left_layout.addWidget(QLabel('Con cuánto pagas:'))
        left_layout.addWidget(self.payment_amount_input)
        left_layout.addWidget(self.change_label)
        left_layout.addWidget(self.add_button)

        discount_layout = QHBoxLayout()
        discount_layout.addWidget(QLabel('Descuento %:'))
        discount_layout.addWidget(self.discount_input)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('Factura'))
        right_layout.addWidget(self.cart_table)
        right_layout.addLayout(discount_layout)
        right_layout.addWidget(self.subtotal_label)
        right_layout.addWidget(self.discount_label)
        right_layout.addWidget(self.tax_label)
        right_layout.addWidget(self.total_label)
        right_layout.addWidget(self.remove_button)
        right_layout.addWidget(self.checkout_button)
        right_layout.addWidget(self.export_pdf_button)
        right_layout.addWidget(self.view_invoice_button)

        content_layout = QHBoxLayout()
        content_layout.addLayout(left_layout, 3)
        content_layout.addLayout(right_layout, 2)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addLayout(content_layout)

        self.refresh()
        self.update_role_permissions()

    def load_clients(self):
        self.client_selector.blockSignals(True)
        self.client_selector.clear()
        self.client_selector.addItem('Cliente no seleccionado', None)
        self.clients = self.client_service.list_clients()
        for client in self.clients:
            self.client_selector.addItem(f'{client.name} ({client.email or "sin email"})', client.id)
        self.client_selector.setCurrentIndex(0)
        self.selected_invoice_client_id = None
        self.client_selector.blockSignals(False)

    def on_client_selected(self):
        client_id = self.client_selector.currentData()
        self.selected_invoice_client_id = client_id
        if client_id is None:
            self.client_name_input.setReadOnly(False)
            self.client_name_input.clear()
            self.client_name_input.setPlaceholderText('Nombre del cliente (opcional, Consumidor Final si no se ingresa)')
        else:
            client = next((c for c in self.clients if c.id == client_id), None)
            if client:
                self.client_name_input.setText(client.name)
                self.client_name_input.setReadOnly(True)
                self.client_name_input.setPlaceholderText('Cliente seleccionado')
            else:
                self.client_name_input.setReadOnly(False)

    def set_current_user(self, user_info: dict):
        self.current_user = user_info
        self.update_role_permissions()

    def refresh(self, keep_invoice: bool = False):
        self.product_search_input.clear()
        self.client_name_input.clear()
        self.apply_tax_checkbox.setChecked(True)
        self.cart_items = []
        self.cart_table.setRowCount(0)
        self.payment_amount_input.setValue(0.00)
        self.discount_input.setValue(0)
        self.selected_invoice_client_id = None
        if not keep_invoice:
            self.current_invoice_number = None
            self.current_invoice_path = None
            self.view_invoice_button.setEnabled(False)
        self.export_pdf_button.setEnabled(False)
        self.update_role_permissions()
        self.update_totals()
        self.update_change()
        self.load_clients()
        self.load_products()

    def load_products(self):
        self.products = self.product_repository.list_all()
        self.display_products(self.products)

    def display_products(self, products):
        self.product_table.setRowCount(0)
        for row, product in enumerate(products):
            self.product_table.insertRow(row)
            self.product_table.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.product_table.setItem(row, 1, QTableWidgetItem(product.name))
            self.product_table.setItem(row, 2, QTableWidgetItem(product.sku))
            self.product_table.setItem(row, 3, QTableWidgetItem(f'{product.price:.2f}'))
            self.product_table.setItem(row, 4, QTableWidgetItem(str(product.stock)))
            self.product_table.setItem(row, 5, QTableWidgetItem(product.category.name if product.category else ''))

    def filter_products(self):
        query = self.product_search_input.text().strip().lower()
        if not query:
            self.display_products(self.products)
            return
        filtered = [p for p in self.products if query in p.name.lower() or query in p.sku.lower()]
        self.display_products(filtered)

    def load_product_selection(self):
        selected = self.product_table.selectedItems()
        if not selected:
            self.selected_product_id = None
            return
        self.selected_product_id = int(selected[0].text())

    def add_product_by_double_click(self, item):
        row = item.row()
        product_id_item = self.product_table.item(row, 0)
        if product_id_item is None:
            return
        self.selected_product_id = int(product_id_item.text())
        self.add_to_cart()

    def add_to_cart(self):
        if not self.selected_product_id:
            QMessageBox.warning(self, 'Error', 'Seleccione un producto para agregar.')
            return
        product = self.product_repository.get_by_id(self.selected_product_id)
        if not product:
            QMessageBox.warning(self, 'Error', 'Producto no encontrado.')
            return
        quantity = 1

        existing_item = next((item for item in self.cart_items if item['product_id'] == product.id), None)
        current_quantity = existing_item['quantity'] if existing_item else 0
        if current_quantity + quantity > product.stock:
            QMessageBox.warning(self, 'Error', 'Cantidad total en carrito excede el stock disponible.')
            return

        if existing_item:
            existing_item['quantity'] += quantity
        else:
            self.cart_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'unit_price': product.price,
                'quantity': quantity,
            })

        self.sync_cart_table()
        self.update_totals()
        self.export_pdf_button.setEnabled(bool(self.cart_items))

    def sync_cart_table(self):
        self.updating_cart_table = True
        self.cart_table.setRowCount(0)
        for row, item in enumerate(self.cart_items):
            self.cart_table.insertRow(row)
            for col, value in enumerate([
                item['product_name'],
                str(item['quantity']),
                f"{item['unit_price']:.2f}",
                f"{item['quantity'] * item['unit_price']:.2f}",
            ]):
                table_item = QTableWidgetItem(value)
                if col != 1:
                    table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)
                self.cart_table.setItem(row, col, table_item)
        self.updating_cart_table = False

    def remove_from_cart(self):
        selected = self.cart_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Error', 'Seleccione un elemento del carrito para quitar.')
            return
        row = selected[0].row()
        self.cart_items.pop(row)
        self.sync_cart_table()
        self.update_totals()
        self.export_pdf_button.setEnabled(bool(self.cart_items))

    def on_cart_item_changed(self, item):
        if self.updating_cart_table or item.column() != 1:
            return
        row = item.row()
        if row < 0 or row >= len(self.cart_items):
            return
        cart_item = self.cart_items[row]
        try:
            new_quantity = int(item.text())
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Ingrese una cantidad válida.')
            self.sync_cart_table()
            return

        if new_quantity <= 0:
            QMessageBox.warning(self, 'Error', 'La cantidad debe ser mayor a cero.')
            self.sync_cart_table()
            return

        product = self.product_repository.get_by_id(cart_item['product_id'])
        if product and new_quantity > product.stock:
            QMessageBox.warning(
                self,
                'Error',
                f'No hay stock suficiente para {product.name}. Stock disponible: {product.stock}',
            )
            self.sync_cart_table()
            return

        cart_item['quantity'] = new_quantity
        self.sync_cart_table()
        self.update_totals()
        self.export_pdf_button.setEnabled(bool(self.cart_items))

    def validate_cart_quantities(self):
        for item in self.cart_items:
            product = self.product_repository.get_by_id(item['product_id'])
            if product and item['quantity'] > product.stock:
                raise ValueError(f'Cantidad en carrito excede el stock de {product.name}.')

    def update_role_permissions(self):
        is_admin = bool(self.current_user and self.current_user.get('role') == 'admin')
        self.remove_button.setEnabled(is_admin)

    def update_change(self):
        total = sum(item['quantity'] * item['unit_price'] for item in self.cart_items)
        discount_percent = self.discount_input.value() / 100.0
        discount_amount = total * discount_percent
        subtotal_after_discount = total - discount_amount
        apply_tax = self.apply_tax_checkbox.isChecked()
        tax = subtotal_after_discount * ITBIS_RATE if apply_tax else 0.0
        total_amount = subtotal_after_discount + tax
        paid_amount = float(self.payment_amount_input.value())
        change_amount = paid_amount - total_amount
        self.change_label.setText(f'Cambio: {change_amount:.2f}')

    def update_totals(self):
        subtotal = sum(item['quantity'] * item['unit_price'] for item in self.cart_items)
        discount_percent = self.discount_input.value() / 100.0
        discount_amount = subtotal * discount_percent
        subtotal_after_discount = subtotal - discount_amount
        apply_tax = self.apply_tax_checkbox.isChecked()
        tax = subtotal_after_discount * ITBIS_RATE if apply_tax else 0.0
        total = subtotal_after_discount + tax

        self.subtotal_label.setText(f'Subtotal: {subtotal:.2f}')
        self.discount_label.setText(f'Descuento: {discount_amount:.2f}')
        self.tax_label.setText(f'ITBIS ({int(ITBIS_RATE*100)}%): {tax:.2f}' if apply_tax else 'ITBIS: 0.00')
        self.total_label.setText(f'Total: {total:.2f}')
        self.update_change()

    def export_invoice_pdf(self, show_message: bool = True) -> str | None:
        if not self.cart_items:
            if show_message:
                QMessageBox.warning(self, 'Error', 'No hay elementos en el carrito para exportar.')
            return None

        if not self.current_invoice_number:
            self.current_invoice_number = self.generate_invoice_number()

        invoice_data = self.build_invoice_data()
        filename = self.build_invoice_filename(invoice_data)
        file_path = generate_invoice_pdf(invoice_data, filename=filename)
        if show_message:
            QMessageBox.information(self, 'Factura PDF', f'Factura generada en:\n{file_path}')

        self.current_invoice_path = file_path
        self.view_invoice_button.setEnabled(True)
        return file_path

    def build_invoice_data(self) -> dict:
        subtotal = sum(item['quantity'] * item['unit_price'] for item in self.cart_items)
        discount_percent = self.discount_input.value() / 100.0
        discount_amount = subtotal * discount_percent
        subtotal_after_discount = subtotal - discount_amount
        apply_tax = self.apply_tax_checkbox.isChecked()
        tax = subtotal_after_discount * ITBIS_RATE if apply_tax else 0.0
        total = subtotal_after_discount + tax
        paid_amount = float(self.payment_amount_input.value())
        change_amount = paid_amount - total
        selected_client = next((c for c in getattr(self, 'clients', []) if c.id == self.selected_invoice_client_id), None)
        client_name = selected_client.name if selected_client else self.client_name_input.text().strip() or 'Consumidor Final'
        return {
            'invoice_number': self.current_invoice_number or self.generate_invoice_number(),
            'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'business_name': get_setting('business_name') or 'Mi Negocio',
            'business_address': get_setting('business_address') or '',
            'business_phone': get_setting('business_phone') or '',
            'business_logo_path': get_setting('business_logo_path') or '',
            'client_name': client_name,
            'cashier': self.current_user['username'] if self.current_user else 'Desconocido',
            'payment_method': self.payment_method_input.currentText(),
            'discount_percent': discount_percent * 100,
            'subtotal': subtotal,
            'discount': discount_amount,
            'tax': tax,
            'tax_applied': apply_tax,
            'total': total,
            'paid_amount': paid_amount,
            'change_amount': change_amount,
            'items': [
                {
                    'name': item['product_name'],
                    'quantity': item['quantity'],
                    'unit_price': item['unit_price'],
                    'total_price': item['quantity'] * item['unit_price'],
                }
                for item in self.cart_items
            ],
        }

    def generate_invoice_number(self) -> str:
        return datetime.utcnow().strftime('FAC%Y%m%d%H%M%S')

    def build_invoice_filename(self, invoice_data: dict) -> str:
        client_name = invoice_data.get('client_name', 'Consumidor Final')
        safe_client = ''.join(
            ch for ch in client_name.strip().lower().replace(' ', '_')
            if ch.isalnum() or ch in ('_', '-')
        ) or 'consumidor_final'
        invoice_number = invoice_data.get('invoice_number', 'sin_numero')
        filename = f'{safe_client}_{invoice_number}.pdf'
        return filename

    def clear_sale_session(self):
        self.cart_items.clear()
        self.sync_cart_table()
        self.current_invoice_number = None
        self.payment_amount_input.setValue(0.00)
        self.discount_input.setValue(0)
        self.apply_tax_checkbox.setChecked(True)
        self.client_name_input.clear()
        self.export_pdf_button.setEnabled(False)
        self.update_totals()
        self.update_change()

    def open_invoice_file(self):
        if not self.current_invoice_path:
            QMessageBox.warning(self, 'Error', 'No hay factura generada para visualizar.')
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.current_invoice_path))

    def finalize_sale(self):
        if not self.current_user:
            QMessageBox.warning(self, 'Error', 'Se requiere iniciar sesión antes de cerrar ventas.')
            return
        if not self.cart_items:
            QMessageBox.warning(self, 'Error', 'El carrito está vacío.')
            return

        self.validate_cart_quantities()
        total = self.build_invoice_data()['total']
        paid_amount = float(self.payment_amount_input.value())
        if paid_amount < total:
            QMessageBox.warning(self, 'Error', 'El monto pagado debe ser igual o mayor al total.')
            return

        try:
            selected_client = next((c for c in getattr(self, 'clients', []) if c.id == self.selected_invoice_client_id), None)
            client_name = selected_client.name if selected_client else self.client_name_input.text().strip() or 'Consumidor Final'
            self.sale_service.create_sale(
                cashier=self.current_user['username'],
                payment_method=self.payment_method_input.currentText(),
                cart_items=self.cart_items,
                discount_percent=self.discount_input.value() / 100.0,
                client_name=client_name,
                apply_tax=self.apply_tax_checkbox.isChecked(),
            )
            pdf_path = self.export_invoice_pdf(show_message=False)
            mensaje = 'La venta se ha procesado correctamente.'
            if pdf_path:
                mensaje += f'\nFactura guardada en:\n{pdf_path}'
                self.view_invoice_button.setEnabled(True)
            QMessageBox.information(self, 'Venta registrada', mensaje)
            self.sale_completed.emit()
            self.refresh(keep_invoice=bool(pdf_path))
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))
