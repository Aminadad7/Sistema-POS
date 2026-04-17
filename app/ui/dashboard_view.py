from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
from PySide6.QtCore import Qt
from app.services.product_service import ProductService
from app.services.client_service import ClientService
from app.services.report_service import ReportService


class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_service = ProductService()
        self.client_service = ClientService()
        self.report_service = ReportService()
        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Panel Principal')
        self.title_label.setObjectName('titleLabel')

        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet('background: white; border-radius: 12px; padding: 18px;')

        self.products_count_label = QLabel('Productos: cargando...')
        self.products_count_label.setStyleSheet('color: #111827; font-size: 14pt; font-weight: bold;')
        self.clients_count_label = QLabel('Clientes: cargando...')
        self.clients_count_label.setStyleSheet('color: #111827; font-size: 14pt; font-weight: bold;')
        self.sales_today_label = QLabel('Ventas hoy: cargando...')
        self.sales_today_label.setStyleSheet('color: #111827; font-size: 14pt; font-weight: bold;')

        summary_layout = QVBoxLayout(self.summary_frame)
        summary_layout.addWidget(self.products_count_label)
        summary_layout.addWidget(self.clients_count_label)
        summary_layout.addWidget(self.sales_today_label)

        self.report_button = QPushButton('Actualizar datos')
        self.report_button.setStyleSheet('background: #2563eb; color: white; border-radius: 6px; padding: 8px;')
        self.report_button.clicked.connect(self.refresh)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.summary_frame)
        layout.addSpacing(12)
        layout.addWidget(self.report_button)
        layout.addStretch(1)

    def set_current_user(self, user_info: dict):
        self.current_user = user_info
        self.refresh()

    def refresh(self):
        products = self.product_service.list_products()
        self.products_count_label.setText(f'Productos registrados: {len(products)}')

        clients = self.client_service.list_clients()
        self.clients_count_label.setText(f'Clientes registrados: {len(clients)}')

        sales_today = self.report_service.sales_today()
        self.sales_today_label.setText(f'Ventas hoy: {len(sales_today)}')
