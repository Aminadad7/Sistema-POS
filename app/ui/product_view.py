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
    QSizePolicy,
    QHeaderView,
)
from PySide6.QtCore import Qt, Signal
from app.services.product_service import ProductService
from app.services.report_service import ReportService


class ProductView(QWidget):
    product_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_service = ProductService()
        self.report_service = ReportService()
        self.current_user = None
        self.selected_product_id = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Gestión de Productos')
        self.title_label.setObjectName('titleLabel')

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Nombre del producto')
        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText('SKU generado automáticamente')
        self.sku_input.setReadOnly(True)
        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix('RD$ ')
        self.price_input.setDecimals(2)
        self.price_input.setRange(0.01, 9999999.99)
        self.price_input.setSingleStep(0.50)
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 999999)
        self.category_input = QComboBox()

        self.save_button = QPushButton('Crear producto')
        self.save_button.clicked.connect(self.save_product)
        self.update_button = QPushButton('Actualizar producto')
        self.update_button.clicked.connect(self.update_product)
        self.new_button = QPushButton('Nuevo producto')
        self.new_button.clicked.connect(self.clear_form)
        self.delete_button = QPushButton('Eliminar selección')
        self.delete_button.clicked.connect(self.delete_product)

        self.permission_message = QLabel('')
        self.permission_message.setStyleSheet('font-size: 11pt;')

        self.daily_sales_label = QLabel('Ventas hoy: RD$ 0.00')
        self.daily_sales_label.setStyleSheet('font-size: 13pt; font-weight: bold;')
        self.monthly_sales_label = QLabel('Ventas mes: RD$ 0.00')
        self.monthly_sales_label.setStyleSheet('font-size: 13pt; font-weight: bold;')

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.sku_input)
        form_layout.addWidget(self.price_input)
        form_layout.addWidget(self.stock_input)
        form_layout.addWidget(self.category_input)
        form_layout.addWidget(self.new_button)
        form_layout.addWidget(self.save_button)
        form_layout.addWidget(self.update_button)
        form_layout.addWidget(self.delete_button)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(['ID', 'Nombre', 'SKU', 'Precio', 'Stock', 'Categoría'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setMinimumHeight(320)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.itemSelectionChanged.connect(self.load_selection)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addLayout(form_layout)
        layout.addWidget(self.permission_message)
        layout.addWidget(self.daily_sales_label)
        layout.addWidget(self.monthly_sales_label)
        layout.addWidget(self.table)

        self.refresh()

    def refresh(self):
        self.apply_permissions()
        self.table.setRowCount(0)
        self.load_sales_totals()
        categories = self.product_service.list_categories()
        self.category_input.clear()
        self.category_input.addItem('Sin categoría', None)
        for category in categories:
            self.category_input.addItem(category.name, category.id)

        products = self.product_service.list_products()
        for row, product in enumerate(products):
            self.table.insertRow(row)
            for col, value in enumerate([
                str(product.id),
                product.name,
                product.sku,
                f'{product.price:.2f}',
                str(product.stock),
                product.category.name if product.category else '',
            ]):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

    def load_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            self.selected_product_id = None
            self.apply_permissions()
            return
        self.selected_product_id = int(selected[0].text())
        product = self.product_service.get_product_by_id(self.selected_product_id)
        if product:
            self.name_input.setText(product.name)
            self.sku_input.setText(product.sku)
            self.price_input.setValue(product.price)
            self.stock_input.setValue(product.stock)
            if product.category_id:
                index = self.category_input.findData(product.category_id)
                if index >= 0:
                    self.category_input.setCurrentIndex(index)
        self.apply_permissions()

    def set_current_user(self, user_info: dict | None):
        self.current_user = user_info
        self.apply_permissions()
        self.load_sales_totals()

    def load_sales_totals(self):
        today = self.report_service.sales_today()
        month = self.report_service.sales_for_month(
            datetime.utcnow().year, datetime.utcnow().month
        )
        daily_total = sum(sale.total for sale in today)
        monthly_total = sum(sale.total for sale in month)
        self.daily_sales_label.setText(f'Ventas hoy: RD$ {daily_total:.2f}')
        self.monthly_sales_label.setText(f'Ventas mes: RD$ {monthly_total:.2f}')

    def apply_permissions(self):
        is_admin = bool(self.current_user and self.current_user.get('role') == 'admin')
        self.name_input.setReadOnly(not is_admin)
        self.sku_input.setReadOnly(True)
        self.price_input.setEnabled(is_admin)
        self.stock_input.setEnabled(is_admin)
        self.category_input.setEnabled(is_admin)
        self.new_button.setEnabled(is_admin)
        self.save_button.setEnabled(is_admin)
        self.update_button.setEnabled(is_admin and self.selected_product_id is not None)
        self.delete_button.setEnabled(is_admin and self.selected_product_id is not None)
        self.permission_message.setText(
            'Solo el administrador puede crear, editar o eliminar productos.' if not is_admin else ''
        )

    def save_product(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            QMessageBox.warning(self, 'Permisos', 'Solo el administrador puede crear productos.')
            return
        if self.selected_product_id:
            QMessageBox.warning(self, 'Error', 'Seleccione "Nuevo producto" para crear un producto nuevo o use "Actualizar producto" para editar uno existente.')
            return
        try:
            name = self.name_input.text()
            price = float(self.price_input.value())
            stock = int(self.stock_input.value())
            category_id = self.category_input.currentData()
            self.product_service.create_product(name, price, stock, category_id)
            QMessageBox.information(self, 'Éxito', 'Producto creado correctamente.')
            self.clear_form()
            self.refresh()
            self.product_changed.emit()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def update_product(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            QMessageBox.warning(self, 'Permisos', 'Solo el administrador puede actualizar productos.')
            return
        if not self.selected_product_id:
            QMessageBox.warning(self, 'Error', 'Seleccione un producto para actualizar.')
            return
        try:
            name = self.name_input.text()
            price = float(self.price_input.value())
            stock = int(self.stock_input.value())
            category_id = self.category_input.currentData()
            self.product_service.update_product(self.selected_product_id, name, price, stock, category_id)
            QMessageBox.information(self, 'Éxito', 'Producto actualizado correctamente.')
            self.clear_form()
            self.refresh()
            self.product_changed.emit()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def delete_product(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            QMessageBox.warning(self, 'Permisos', 'Solo el administrador puede eliminar productos.')
            return
        if not self.selected_product_id:
            QMessageBox.warning(self, 'Error', 'Seleccione un producto para eliminar.')
            return
        try:
            self.product_service.delete_product(self.selected_product_id)
            QMessageBox.information(self, 'Éxito', 'Producto eliminado.')
            self.clear_form()
            self.refresh()
            self.product_changed.emit()
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def clear_form(self):
        self.selected_product_id = None
        self.name_input.clear()
        self.sku_input.clear()
        self.price_input.setValue(0.00)
        self.stock_input.setValue(0)
        self.category_input.setCurrentIndex(0)
