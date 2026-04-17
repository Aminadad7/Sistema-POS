from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView
from app.services.product_service import ProductService
from app.services.client_service import ClientService
from app.services.report_service import ReportService
from app.utils.settings_manager import get_setting


class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.product_service = ProductService()
        self.client_service = ClientService()
        self.report_service = ReportService()
        self.current_user = None
        self.theme = get_setting('theme') or 'dark'
        self.setup_ui()

    def setup_ui(self):
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(80, 80)
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel('Panel Principal')
        self.title_label.setObjectName('titleLabel')

        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet(self.card_frame_style())

        self.products_count_label = QLabel('Productos: cargando...')
        self.clients_count_label = QLabel('Clientes: cargando...')
        self.sales_today_label = QLabel('Ventas hoy: cargando...')
        for label in [self.products_count_label, self.clients_count_label, self.sales_today_label]:
            label.setStyleSheet(self.summary_label_style())

        summary_layout = QHBoxLayout(self.summary_frame)
        self.products_card = self.create_stat_card('Productos registrados', self.products_count_label)
        self.clients_card = self.create_stat_card('Clientes registrados', self.clients_count_label)
        self.sales_card = self.create_stat_card('Ventas hoy', self.sales_today_label)
        summary_layout.addWidget(self.products_card)
        summary_layout.addWidget(self.clients_card)
        summary_layout.addWidget(self.sales_card)

        self.product_stats_frame = QFrame()
        self.product_stats_frame.setStyleSheet(self.card_frame_style())
        self.product_stats_table = QTableWidget(0, 3)
        self.product_stats_table.setHorizontalHeaderLabels(['Producto', 'Vendidos', '%'])
        self.configure_table(self.product_stats_table)
        self.setup_table_headers(self.product_stats_table, ['Producto', 'Vendidos', '%'])

        self.client_stats_frame = QFrame()
        self.client_stats_frame.setStyleSheet(self.card_frame_style())
        self.client_stats_table = QTableWidget(0, 3)
        # self.client_stats_table.setHorizontalHeaderLabels(['Cliente', 'Ventas', 'Total RD$'])
        self.configure_table(self.client_stats_table)
        self.setup_table_headers(self.client_stats_table, ['Cliente', 'Ventas', 'Total RD$'])

        self.monthly_sales_frame = QFrame()
        self.monthly_sales_frame.setStyleSheet(self.card_frame_style())
        self.monthly_sales_table = QTableWidget(0, 3)
        self.monthly_sales_table.setHorizontalHeaderLabels(['Mes', 'Total RD$', 'Ventas'])
        self.configure_table(self.monthly_sales_table)
        self.setup_table_headers(self.monthly_sales_table, ['Mes', 'Total RD$', 'Ventas'])

        self.report_button = QPushButton('Actualizar datos')
        self.report_button.setStyleSheet('background: #2563eb; color: white; border-radius: 6px; padding: 8px;')
        self.report_button.clicked.connect(self.refresh)

        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.product_stats_frame, 2)
        stats_layout.addWidget(self.client_stats_frame, 2)
        stats_layout.addWidget(self.monthly_sales_frame, 2)

        product_layout = QVBoxLayout(self.product_stats_frame)
        self.product_section_label = QLabel('Productos más vendidos')
        self.product_section_label.setStyleSheet(self.section_title_style())
        product_layout.addWidget(self.product_section_label)
        product_layout.addWidget(self.product_stats_table)

        client_layout = QVBoxLayout(self.client_stats_frame)
        self.client_section_label = QLabel('Relación de clientes')
        self.client_section_label.setStyleSheet(self.section_title_style())
        client_layout.addWidget(self.client_section_label)
        client_layout.addWidget(self.client_stats_table)

        monthly_layout = QVBoxLayout(self.monthly_sales_frame)
        self.monthly_section_label = QLabel('Ventas por mes')
        self.monthly_section_label.setStyleSheet(self.section_title_style())
        monthly_layout.addWidget(self.monthly_section_label)
        monthly_layout.addWidget(self.monthly_sales_table)

        layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.logo_label)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1)
        layout.addLayout(header_layout)
        layout.addWidget(self.summary_frame)
        layout.addSpacing(12)
        layout.addLayout(stats_layout)
        layout.addSpacing(12)
        layout.addWidget(self.report_button)
        layout.addStretch(1)

        self.apply_theme(self.theme)
        self.load_logo()

    def set_current_user(self, user_info: dict):
        self.current_user = user_info
        self.refresh()

    def load_logo(self):
        logo_path = get_setting('business_logo_path') or ''
        if logo_path:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.logo_label.setVisible(True)
                return
        self.logo_label.clear()
        self.logo_label.setVisible(False)

    def refresh(self):
        products = self.product_service.list_products()
        self.products_count_label.setText(f'{len(products)}')

        clients = self.client_service.list_clients()
        self.clients_count_label.setText(f'{len(clients)}')

        sales_today = self.report_service.sales_today()
        self.sales_today_label.setText(f'{len(sales_today)}')

        self.populate_product_stats()
        self.populate_client_stats()
        self.populate_monthly_sales()

    def configure_table(self, table: QTableWidget):
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setMinimumHeight(220)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setVisible(True)
        table.horizontalHeader().setHighlightSections(False)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setStyleSheet(self.table_style())
        table.horizontalHeader().setSectionsClickable(False)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def setup_table_headers(self, table: QTableWidget, headers: list[str]):
        for index, header_text in enumerate(headers):
            table.setHorizontalHeaderItem(index, QTableWidgetItem(header_text))
        table.horizontalHeader().setVisible(True)
        table.horizontalHeader().setStyleSheet(self.header_style())

    def create_stat_card(self, title: str, value_label: QLabel) -> QFrame:
        card = QFrame()
        card.setStyleSheet(self.card_frame_style())
        title_label = QLabel(title)
        title_label.setStyleSheet(self.subtitle_label_style())
        value_label.setAlignment(Qt.AlignCenter)
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        return card

    def create_bar_text(self, value: float, maximum: float, width: int = 18) -> str:
        if maximum <= 0:
            return '0%'
        ratio = min(1.0, value / maximum)
        filled = int(ratio * width)
        bar = '█' * filled + '░' * (width - filled)
        return f'{int(ratio * 100):3d}% {bar}'

    def is_dark_theme(self) -> bool:
        return get_setting('theme') == 'dark'

    def card_frame_style(self) -> str:
        if self.is_dark_theme():
            return 'background: #111827; color: #e2e8f0; border-radius: 12px; padding: 14px;'
        return 'background: #ffffff; color: #0f172a; border-radius: 12px; padding: 14px;'

    def summary_label_style(self) -> str:
        if self.is_dark_theme():
            return 'color: #e2e8f0; font-size: 14pt; font-weight: bold;'
        return 'color: #111827; font-size: 14pt; font-weight: bold;'

    def subtitle_label_style(self) -> str:
        if self.is_dark_theme():
            return 'color: #cbd5e1; font-size: 11pt;'
        return 'color: #6b7280; font-size: 11pt;'

    def section_title_style(self) -> str:
        if self.is_dark_theme():
            return 'color: #e2e8f0; font-size: 13pt; font-weight: bold;'
        return 'color: #0f172a; font-size: 13pt; font-weight: bold;'

    def apply_theme(self, theme: str):
        self.theme = theme
        self.summary_frame.setStyleSheet(self.card_frame_style())
        self.products_card.setStyleSheet(self.card_frame_style())
        self.clients_card.setStyleSheet(self.card_frame_style())
        self.sales_card.setStyleSheet(self.card_frame_style())
        self.product_stats_frame.setStyleSheet(self.card_frame_style())
        self.client_stats_frame.setStyleSheet(self.card_frame_style())
        self.monthly_sales_frame.setStyleSheet(self.card_frame_style())
        for label in [self.products_count_label, self.clients_count_label, self.sales_today_label]:
            label.setStyleSheet(self.summary_label_style())
        for label in [self.product_section_label, self.client_section_label, self.monthly_section_label]:
            label.setStyleSheet(self.section_title_style())
        for table in [self.product_stats_table, self.client_stats_table, self.monthly_sales_table]:
            table.setStyleSheet(self.table_style())
            table.horizontalHeader().setStyleSheet(self.header_style())

    def table_style(self) -> str:
        if self.is_dark_theme():
            return '''
                QTableWidget {
                    background: #111827;
                    alternate-background-color: #1e293b;
                    color: #e2e8f0;
                    gridline-color: #334155;
                }
                QHeaderView::section {
                    background: #1e293b;
                    color: #e2e8f0;
                    padding: 8px;
                    border: 1px solid #334155;
                }
            '''
        return '''
            QTableWidget {
                background: #ffffff;
                alternate-background-color: #f8fafc;
                color: #0f172a;
                gridline-color: #cbd5e1;
            }
            QHeaderView::section {
                background: #e2e8f0;
                color: #0f172a;
                padding: 8px;
                border: 1px solid #cbd5e1;
            }
        '''

    def header_style(self) -> str:
        if self.is_dark_theme():
            return '''
                QHeaderView::section {
                    background: #1e293b;
                    color: #e2e8f0;
                    font-weight: bold;
                }
            '''
        return '''
            QHeaderView::section {
                background: #e2e8f0;
                color: #0f172a;
                font-weight: bold;
            }
        '''

    def populate_product_stats(self):
        data = self.report_service.product_sales_summary()
        max_qty = max((qty for _, qty, _ in data), default=1)
        self.product_stats_table.setRowCount(0)
        for row, (product_name, qty, revenue) in enumerate(data):
            self.product_stats_table.insertRow(row)
            self.product_stats_table.setItem(row, 0, QTableWidgetItem(product_name))
            self.product_stats_table.setItem(row, 1, QTableWidgetItem(str(qty)))
            self.product_stats_table.setItem(row, 2, QTableWidgetItem(self.create_bar_text(qty, max_qty)))

    def populate_client_stats(self):
        data = self.report_service.client_sales_summary()
        max_sales = max((sales for _, sales, _ in data), default=1)
        self.client_stats_table.setRowCount(0)
        for row, (client_name, sales_count, total) in enumerate(data):
            self.client_stats_table.insertRow(row)
            self.client_stats_table.setItem(row, 0, QTableWidgetItem(client_name))
            self.client_stats_table.setItem(row, 1, QTableWidgetItem(str(sales_count)))
            self.client_stats_table.setItem(row, 2, QTableWidgetItem(f'RD$ {total:.2f}'))

    def populate_monthly_sales(self):
        data = self.report_service.monthly_sales_summary(months=6)
        self.monthly_sales_table.setRowCount(0)
        for row, (period, total, count) in enumerate(data):
            self.monthly_sales_table.insertRow(row)
            self.monthly_sales_table.setItem(row, 0, QTableWidgetItem(period))
            self.monthly_sales_table.setItem(row, 1, QTableWidgetItem(f'RD$ {total:.2f}'))
            self.monthly_sales_table.setItem(row, 2, QTableWidgetItem(str(count)))
