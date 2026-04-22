from datetime import datetime
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QHeaderView
from PySide6.QtGui import QDesktopServices
from app.services.report_service import ReportService


class ReportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.report_service = ReportService()
        self.setup_ui()

    def setup_ui(self):
        self.title_label = QLabel('Reportes de Ventas')
        self.title_label.setObjectName('titleLabel')

        self.today_button = QPushButton('Ventas hoy')
        self.today_button.clicked.connect(self.load_sales_today)

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(datetime.utcnow().date())
        self.date_from.setDisplayFormat('MMMM yyyy')

        self.month_button = QPushButton('Ventas por mes')
        self.month_button.clicked.connect(self.load_sales_for_month)
        self.month_button.setEnabled(False)
        self.month_button.setToolTip('Solo administradores pueden ver ventas por mes')

        self.all_invoices_button = QPushButton('Todas las facturas')
        self.all_invoices_button.clicked.connect(self.load_all_sales)

        self.download_invoice_button = QPushButton('Descargar factura seleccionada')
        self.download_invoice_button.setEnabled(False)
        self.download_invoice_button.clicked.connect(self.download_selected_invoice)

        self.sales_summary_label = QLabel('Resumen de ventas')
        self.sales_summary_label.setStyleSheet('font-size: 14pt; font-weight: bold; margin-top: 12px;')

        self.total_sales_label = QLabel('Total ventas: RD$ 0.00')
        self.total_discounts_label = QLabel('Total descuentos: RD$ 0.00')
        self.total_tax_label = QLabel('Total ITBIS: RD$ 0.00')
        self.sale_count_label = QLabel('Cantidad de ventas: 0')
        self.current_period_label = QLabel('Periodo actual: Hoy')
        for label in [self.total_sales_label, self.total_discounts_label, self.total_tax_label, self.sale_count_label, self.current_period_label]:
            label.setStyleSheet('font-size: 13pt;')

        self.sales_table = QTableWidget(0, 6)
        self.sales_table.setHorizontalHeaderLabels(['ID', 'Fecha', 'Cliente', 'Subtotal', 'Descuento', 'Total'])
        self.sales_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sales_table.setMinimumHeight(320)
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.sales_table.horizontalHeader().setStretchLastSection(True)
        self.sales_table.horizontalHeader().setMinimumSectionSize(100)
        self.sales_table.verticalHeader().setVisible(False)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setStyleSheet('font-size: 12pt;')
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.sales_table.setWordWrap(False)
        self.sales_table.itemSelectionChanged.connect(self.on_sale_selected)

        self.top_products_table = QTableWidget(0, 3)
        self.top_products_table.setHorizontalHeaderLabels(['Producto', 'Cantidad vendida', 'Gráfico %'])
        self.top_products_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.top_products_table.setMinimumHeight(240)
        self.top_products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.top_products_table.horizontalHeader().setStretchLastSection(True)
        self.top_products_table.horizontalHeader().setMinimumSectionSize(140)
        self.top_products_table.verticalHeader().setVisible(False)
        self.top_products_table.setAlternatingRowColors(True)
        self.top_products_table.setStyleSheet('font-size: 12pt;')
        self.top_products_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.top_products_table.setWordWrap(False)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.today_button)
        buttons_layout.addWidget(self.date_from)
        buttons_layout.addWidget(self.month_button)
        buttons_layout.addWidget(self.all_invoices_button)
        buttons_layout.addWidget(self.download_invoice_button)

        summary_layout = QVBoxLayout()
        summary_layout.addWidget(self.sales_summary_label)
        summary_layout.addWidget(self.current_period_label)
        summary_layout.addWidget(self.sale_count_label)
        summary_layout.addWidget(self.total_sales_label)
        summary_layout.addWidget(self.total_discounts_label)
        summary_layout.addWidget(self.total_tax_label)

        self.top_products_label = QLabel('Productos más vendidos')
        self.top_products_label.setStyleSheet('font-size: 14pt; font-weight: bold;')

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addLayout(buttons_layout)
        layout.addLayout(summary_layout)
        layout.addWidget(self.sales_table)
        layout.addWidget(self.top_products_label)
        layout.addWidget(self.top_products_table)

        self.refresh()

    def set_current_user(self, user_info: dict | None):
        self.current_user = user_info
        self.month_button.setEnabled(bool(user_info and user_info.get('role') == 'admin'))
        if not self.month_button.isEnabled():
            self.month_button.setToolTip('Solo administradores pueden ver ventas por mes')
        else:
            self.month_button.setToolTip('Filtrar ventas por mes seleccionado')

    def refresh(self):
        self.load_sales_today()
        self.load_top_products()

    def load_sales_today(self):
        summary = self.report_service.sales_today_summary()
        self.current_period_label.setText('Periodo actual: Hoy')
        self.populate_sales_table(summary['sales'])
        self.populate_sales_summary(summary)

    def load_sales_for_month(self):
        if not self.current_user or self.current_user.get('role') != 'admin':
            self.sales_table.setRowCount(0)
            self.populate_sales_summary({'count': 0, 'total_sales': 0.0, 'total_discounts': 0.0, 'total_tax': 0.0})
            self.current_period_label.setText('Periodo actual: No autorizado')
            return
        date_selected = self.date_from.date().toPython()
        summary = self.report_service.sales_for_month_summary(date_selected.year, date_selected.month)
        self.current_period_label.setText(f'Periodo actual: {date_selected.strftime("%B %Y")}')
        self.populate_sales_table(summary['sales'])
        self.populate_sales_summary(summary)

    def load_all_sales(self):
        sales = self.report_service.list_all_sales()
        self.current_period_label.setText('Periodo actual: Todas las facturas')
        self.populate_sales_table(sales)
        self.populate_sales_summary({
            'count': len(sales),
            'total_sales': sum(sale.total for sale in sales),
            'total_discounts': sum(max(0.0, sale.subtotal + sale.tax - sale.total) for sale in sales),
            'total_tax': sum(sale.tax for sale in sales),
        })

    def on_sale_selected(self):
        self.download_invoice_button.setEnabled(bool(self.sales_table.selectedItems()))

    def download_selected_invoice(self):
        selected_items = self.sales_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Factura no seleccionada', 'Seleccione una factura para descargar.')
            return
        sale_id = int(self.sales_table.item(selected_items[0].row(), 0).text())
        sale = self.report_service.get_sale_by_id(sale_id)
        if sale is None:
            QMessageBox.warning(self, 'Error', 'No se encontró la venta seleccionada.')
            return
        invoice_data = self.report_service.build_invoice_data_from_sale(sale)
        from app.utils.pdf_generator import generate_invoice_pdf
        filename = f'{invoice_data["client_name"].strip().replace(" ", "_")}_{invoice_data["invoice_number"]}.pdf'
        file_path = generate_invoice_pdf(invoice_data, filename=filename)
        QMessageBox.information(self, 'Factura descargada', f'Factura generada en:\n{file_path}')
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def populate_sales_summary(self, summary: dict):
        self.sale_count_label.setText(f'Cantidad de ventas: {summary["count"]}')
        self.total_sales_label.setText(f'Total ventas: RD$ {summary["total_sales"]:.2f}')
        self.total_discounts_label.setText(f'Total descuentos: RD$ {summary["total_discounts"]:.2f}')
        self.total_tax_label.setText(f'Total ITBIS: RD$ {summary["total_tax"]:.2f}')

    def populate_sales_table(self, sales):
        self.sales_table.setRowCount(0)
        for row, sale in enumerate(sales):
            discount_amount = max(0.0, sale.subtotal + sale.tax - sale.total)
            self.sales_table.insertRow(row)
            self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale.id)))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale.created_at.strftime('%Y-%m-%d %H:%M')))
            self.sales_table.setItem(row, 2, QTableWidgetItem(sale.client_name or 'Consumidor final'))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f'{sale.subtotal:.2f}'))
            self.sales_table.setItem(row, 4, QTableWidgetItem(f'{discount_amount:.2f}'))
            self.sales_table.setItem(row, 5, QTableWidgetItem(f'{sale.total:.2f}'))

    def create_bar_graph(self, value: int, maximum: int, width: int = 18) -> str:
        if maximum <= 0:
            return '0%'
        percent = int((value / maximum) * 100)
        filled = int((value / maximum) * width)
        bar = '█' * filled + '░' * (width - filled)
        return f'{percent:3d}% {bar}'

    def load_top_products(self):
        products = self.report_service.top_products()
        self.top_products_table.setRowCount(0)
        quantities = [count for _, count in products]
        max_quantity = max(quantities, default=0)
        total_sold = sum(quantities)
        for row, (name, count) in enumerate(products):
            percentage = (count / total_sold * 100) if total_sold else 0.0
            graph_text = self.create_bar_graph(count, max_quantity)
            self.top_products_table.insertRow(row)
            self.top_products_table.setItem(row, 0, QTableWidgetItem(name))
            self.top_products_table.setItem(row, 1, QTableWidgetItem(str(count)))
            graph_item = QTableWidgetItem(f'{graph_text}  ({percentage:.0f}%)')
            graph_item.setTextAlignment(Qt.AlignCenter)
            self.top_products_table.setItem(row, 2, graph_item)
